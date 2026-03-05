from unittest.mock import MagicMock, patch

from spec_weaver.adapters.doorstop import (
    MultiTree,
    _build_child_index,
    check_children_suspect,
    check_suspect_cross_root,
    clear_children_stamps,
    clear_suspect_cross_root,
    get_item_warnings,
    get_specs,
    is_suspect,
)


class MockDoorstopItem:
    def __init__(self, uid, prefix, active=True, testable=True):
        self.uid = uid
        self.document = MagicMock()
        self.document.prefix = prefix
        self.active = active
        self.testable = testable

    def get(self, key, default=None):
        if key == "testable":
            return self.testable
        return getattr(self, key, default)

class MockDoorstopDocument:
    def __init__(self, items):
        self.items = items
        self.prefix = "SPEC" if items and "SPEC" in items[0].uid else "REQ"

    def __iter__(self):
        return iter(self.items)


class MockDoorstopTree:
    """_build_all_trees が返す Tree 相当のモック。"""

    def __init__(self, documents):
        self._documents = documents

    def __iter__(self):
        return iter(self._documents)


@patch("spec_weaver.adapters.doorstop._build_all_trees")
def test_get_specs_filtering(mock_build_trees, tmp_path):
    # Doorstopのツリーをシミュレート
    items = [
        MockDoorstopItem(
            "SPEC-001", "SPEC", active=True, testable=True
        ),  # 抽出されるべき
        MockDoorstopItem(
            "SPEC-002", "SPEC", active=False, testable=True
        ),  # 削除済み(active=False)なので除外
        MockDoorstopItem(
            "SPEC-003", "SPEC", active=True, testable=False
        ),  # テスト不要(testable=False)なので除外
        MockDoorstopItem(
            "REQ-001", "REQ", active=True, testable=True
        ),  # プレフィックス違いなので除外
    ]
    mock_build_trees.return_value = [MockDoorstopTree([MockDoorstopDocument(items)])]

    # 実行と検証
    specs = get_specs(repo_root=tmp_path, prefix="SPEC")

    assert specs == {"SPEC-001"}


# ---------------------------------------------------------------------------
# get_item_warnings / is_suspect テスト
# ---------------------------------------------------------------------------


class MockWarningItem:
    """cleared / reviewed を制御可能な Mock Item。"""

    def __init__(self, cleared=True, reviewed=True, links=None):
        self._cleared = cleared
        self._reviewed = reviewed
        self.links = links or []

    @property
    def cleared(self):
        return self._cleared

    @property
    def reviewed(self):
        return self._reviewed


def test_get_item_warnings_normal():
    """正常: 警告なし"""
    item = MockWarningItem(cleared=True, reviewed=True)
    w = get_item_warnings(item)
    assert w.has_suspect_links is False
    assert w.has_unreviewed_changes is False
    assert w.has_any_warning is False


def test_get_item_warnings_suspect_link_only():
    """suspect link のみ"""
    item = MockWarningItem(cleared=False, reviewed=True, links=["REQ-001"])
    w = get_item_warnings(item)
    assert w.has_suspect_links is True
    assert w.has_unreviewed_changes is False
    assert w.has_any_warning is True


def test_get_item_warnings_unreviewed_only():
    """unreviewed のみ"""
    item = MockWarningItem(cleared=True, reviewed=False)
    w = get_item_warnings(item)
    assert w.has_suspect_links is False
    assert w.has_unreviewed_changes is True
    assert w.has_any_warning is True


def test_get_item_warnings_both():
    """suspect link + unreviewed"""
    item = MockWarningItem(cleared=False, reviewed=False, links=["REQ-001"])
    w = get_item_warnings(item)
    assert w.has_suspect_links is True
    assert w.has_unreviewed_changes is True
    assert w.has_any_warning is True


def test_get_item_warnings_fallback():
    """属性が存在しない場合のフォールバック"""

    class EmptyItem:
        pass

    w = get_item_warnings(EmptyItem())
    assert w.has_any_warning is False


def test_is_suspect_backward_compat():
    """is_suspect は get_item_warnings の後方互換ラッパー"""
    assert is_suspect(MockWarningItem(cleared=True, reviewed=True)) is False
    assert is_suspect(MockWarningItem(cleared=False, reviewed=True)) is True
    assert is_suspect(MockWarningItem(cleared=True, reviewed=False)) is True
    assert is_suspect(MockWarningItem(cleared=False, reviewed=False)) is True


# ---------------------------------------------------------------------------
# MultiTree テスト
# ---------------------------------------------------------------------------


class MockTreeWithDocument:
    """document 属性と __iter__ を持つ Tree モック。"""

    def __init__(self, docs):
        self.document = docs[0] if docs else None
        self._docs = docs

    def __iter__(self):
        return iter(self._docs)

    def find_item(self, item_id):
        for doc in self._docs:
            for item in doc:
                if str(item.uid) == item_id:
                    return item
        return None


def test_multi_tree_iterates_all_docs():
    """MultiTree が複数ツリーのドキュメントをすべて列挙する。"""
    items_a = [MockDoorstopItem("REQ-001", "REQ")]
    items_b = [MockDoorstopItem("ADR-001", "ADR")]
    doc_a = MockDoorstopDocument(items_a)
    doc_b = MockDoorstopDocument(items_b)
    tree_a = MockDoorstopTree([doc_a])
    tree_b = MockDoorstopTree([doc_b])

    multi = MultiTree([tree_a, tree_b])
    docs = list(multi)

    assert doc_a in docs
    assert doc_b in docs
    assert len(docs) == 2


def test_multi_tree_find_item_across_trees():
    """MultiTree.find_item が複数ツリーをまたいでアイテムを検索する。"""
    item_a = MockDoorstopItem("REQ-001", "REQ")
    item_b = MockDoorstopItem("ADR-001", "ADR")

    doc_a = MockDoorstopDocument([item_a])
    doc_b = MockDoorstopDocument([item_b])
    tree_a = MockTreeWithDocument([doc_a])
    tree_b = MockTreeWithDocument([doc_b])

    multi = MultiTree([tree_a, tree_b])

    assert multi.find_item("REQ-001") is item_a
    assert multi.find_item("ADR-001") is item_b
    assert multi.find_item("NOT-EXIST") is None


def test_multi_tree_single_root_is_transparent():
    """単一ルートの MultiTree は通常の Tree と同等にふるまう。"""
    items = [MockDoorstopItem("REQ-001", "REQ"), MockDoorstopItem("SPEC-001", "SPEC")]
    doc = MockDoorstopDocument(items)
    tree = MockDoorstopTree([doc])
    multi = MultiTree([tree])

    docs = list(multi)
    assert len(docs) == 1
    assert docs[0] is doc
    assert multi.trees == [tree]


# ---------------------------------------------------------------------------
# クロスルート suspect テスト用モック
# ---------------------------------------------------------------------------


class MockStamp:
    """Doorstop Stamp のモック。"""

    def __init__(self, value: str):
        self._value = value

    def __eq__(self, other):
        if isinstance(other, MockStamp):
            return self._value == other._value
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def __str__(self):
        return self._value

    def __repr__(self):
        return f"MockStamp({self._value!r})"


class MockLinkUID:
    """Doorstop の UID（リンク要素）のモック。stamp 属性を持つ。"""

    def __init__(self, uid: str, stamp: MockStamp):
        self._uid = uid
        self.stamp = stamp

    def __str__(self):
        return self._uid


class MockCrossRootItem:
    """クロスルート suspect テスト用の Item モック。"""

    def __init__(
        self,
        uid: str,
        links: list | None = None,
        stamp_value: str = "current",
        active: bool = True,
        reviewed: bool = True,
        child_stamps: dict | None = None,
    ):
        self.uid = uid
        self.links = links or []
        self._stamp_value = stamp_value
        self.active = active
        self._reviewed = reviewed
        self._data = {}
        if child_stamps is not None:
            self._data["child_stamps"] = child_stamps
        self._saved = False

    def stamp(self):
        return MockStamp(self._stamp_value)

    @property
    def reviewed(self):
        return self._reviewed

    def get(self, key, default=None):
        if key == "child_stamps":
            return self._data.get("child_stamps", default)
        return default

    def set(self, key, value):
        self._data[key] = value

    def save(self):
        self._saved = True


class MockCrossRootDocument:
    """クロスルート用 Document モック。"""

    def __init__(self, items: list):
        self.items = items

    def __iter__(self):
        return iter(self.items)


class MockCrossRootTree:
    """クロスルート用 Tree モック。"""

    def __init__(self, docs: list):
        self._docs = docs

    def __iter__(self):
        return iter(self._docs)


# ---------------------------------------------------------------------------
# check_suspect_cross_root テスト
# ---------------------------------------------------------------------------


def _make_multi_tree(items_by_tree: list[list]) -> MultiTree:
    """items_by_tree: [[item, ...], [item, ...]] → MultiTree を構築。"""
    trees = []
    for item_list in items_by_tree:
        doc = MockCrossRootDocument(item_list)
        tree = MockTreeWithDocument([doc])
        trees.append(tree)
    return MultiTree(trees)


def test_cross_root_suspect_no_issues():
    """リンク先の stamp が一致 → suspect なし。"""
    parent = MockCrossRootItem("QA-001", stamp_value="abc")
    link = MockLinkUID("QA-001", stamp=MockStamp("abc"))
    child = MockCrossRootItem("BDD-001", links=[link])

    multi = _make_multi_tree([[parent], [child]])
    suspects, broken = check_suspect_cross_root(multi, child)

    assert suspects == []
    assert broken == []


def test_cross_root_suspect_stamp_mismatch():
    """リンク先の stamp が不一致 → suspect 検出。"""
    parent = MockCrossRootItem("QA-001", stamp_value="new_hash")
    link = MockLinkUID("QA-001", stamp=MockStamp("old_hash"))
    child = MockCrossRootItem("BDD-001", links=[link])

    multi = _make_multi_tree([[parent], [child]])
    suspects, broken = check_suspect_cross_root(multi, child)

    assert suspects == ["QA-001"]
    assert broken == []


def test_cross_root_suspect_broken_link():
    """リンク先が見つからない → broken link として報告。"""
    link = MockLinkUID("GONE-001", stamp=MockStamp("x"))
    child = MockCrossRootItem("BDD-001", links=[link])

    multi = _make_multi_tree([[child]])
    suspects, broken = check_suspect_cross_root(multi, child)

    assert suspects == []
    assert broken == ["GONE-001"]


def test_cross_root_suspect_mixed():
    """suspect + broken link が混在するケース。"""
    parent_ok = MockCrossRootItem("QA-001", stamp_value="same")
    parent_changed = MockCrossRootItem("QA-002", stamp_value="new")
    link_ok = MockLinkUID("QA-001", stamp=MockStamp("same"))
    link_suspect = MockLinkUID("QA-002", stamp=MockStamp("old"))
    link_broken = MockLinkUID("GONE-001", stamp=MockStamp("x"))
    child = MockCrossRootItem("BDD-001", links=[link_ok, link_suspect, link_broken])

    multi = _make_multi_tree([[parent_ok, parent_changed], [child]])
    suspects, broken = check_suspect_cross_root(multi, child)

    assert suspects == ["QA-002"]
    assert broken == ["GONE-001"]


# ---------------------------------------------------------------------------
# check_children_suspect テスト
# ---------------------------------------------------------------------------


def test_children_suspect_no_children():
    """子がいない → 空リスト。"""
    parent = MockCrossRootItem("QA-001")
    result = check_children_suspect(parent, {})
    assert result == []


def test_children_suspect_not_registered():
    """child_stamps に未登録 → 保存済みハッシュなしのためスキップ（suspect にしない）。"""
    parent = MockCrossRootItem("QA-001", child_stamps={})
    child = MockCrossRootItem("BDD-001", stamp_value="abc")
    child_index = {"QA-001": [child]}

    result = check_children_suspect(parent, child_index)
    assert result == []


def test_children_suspect_stamp_match():
    """child_stamps が一致 → suspect なし。"""
    parent = MockCrossRootItem("QA-001", child_stamps={"BDD-001": "abc"})
    child = MockCrossRootItem("BDD-001", stamp_value="abc")
    child_index = {"QA-001": [child]}

    result = check_children_suspect(parent, child_index)
    assert result == []


def test_children_suspect_stamp_mismatch():
    """child_stamps が不一致 → suspect。"""
    parent = MockCrossRootItem("QA-001", child_stamps={"BDD-001": "old"})
    child = MockCrossRootItem("BDD-001", stamp_value="new")
    child_index = {"QA-001": [child]}

    result = check_children_suspect(parent, child_index)
    assert result == ["BDD-001"]


# ---------------------------------------------------------------------------
# _build_child_index テスト
# ---------------------------------------------------------------------------


def test_build_child_index():
    """リンクから逆引きインデックスが正しく構築される。"""
    link_qa = MockLinkUID("QA-001", stamp=MockStamp("x"))
    link_qa2 = MockLinkUID("QA-001", stamp=MockStamp("x"))
    link_vis = MockLinkUID("VIS-001", stamp=MockStamp("y"))
    bdd1 = MockCrossRootItem("BDD-001", links=[link_qa])
    bdd2 = MockCrossRootItem("BDD-002", links=[link_qa2, link_vis])
    parent_qa = MockCrossRootItem("QA-001")
    parent_vis = MockCrossRootItem("VIS-001")

    multi = _make_multi_tree([[parent_qa, parent_vis], [bdd1, bdd2]])
    index = _build_child_index(multi)

    assert len(index["QA-001"]) == 2
    assert bdd1 in index["QA-001"]
    assert bdd2 in index["QA-001"]
    assert index["VIS-001"] == [bdd2]


def test_build_child_index_skips_inactive():
    """inactive なアイテムは逆引きに含めない。"""
    link = MockLinkUID("QA-001", stamp=MockStamp("x"))
    inactive = MockCrossRootItem("BDD-099", links=[link], active=False)
    parent = MockCrossRootItem("QA-001")

    multi = _make_multi_tree([[parent], [inactive]])
    index = _build_child_index(multi)

    assert "QA-001" not in index


# ---------------------------------------------------------------------------
# clear_suspect_cross_root テスト
# ---------------------------------------------------------------------------


def test_clear_suspect_cross_root_updates_stamp():
    """上方向 clear: リンクの stamp が親の最新値に更新される。"""
    parent = MockCrossRootItem("QA-001", stamp_value="new_hash")
    link = MockLinkUID("QA-001", stamp=MockStamp("old_hash"))
    child = MockCrossRootItem("BDD-001", links=[link])

    multi = _make_multi_tree([[parent], [child]])
    result = clear_suspect_cross_root(multi, child)

    assert result is True
    assert link.stamp == MockStamp("new_hash")
    assert child._saved is True


def test_clear_suspect_cross_root_no_change():
    """stamp が一致 → 更新なし。"""
    parent = MockCrossRootItem("QA-001", stamp_value="same")
    link = MockLinkUID("QA-001", stamp=MockStamp("same"))
    child = MockCrossRootItem("BDD-001", links=[link])

    multi = _make_multi_tree([[parent], [child]])
    result = clear_suspect_cross_root(multi, child)

    assert result is False
    assert child._saved is False


def test_clear_suspect_cross_root_with_targets():
    """targets 指定で特定リンクのみ更新。"""
    parent1 = MockCrossRootItem("QA-001", stamp_value="new1")
    parent2 = MockCrossRootItem("QA-002", stamp_value="new2")
    link1 = MockLinkUID("QA-001", stamp=MockStamp("old1"))
    link2 = MockLinkUID("QA-002", stamp=MockStamp("old2"))
    child = MockCrossRootItem("BDD-001", links=[link1, link2])

    multi = _make_multi_tree([[parent1, parent2], [child]])
    result = clear_suspect_cross_root(multi, child, targets={"QA-001"})

    assert result is True
    assert link1.stamp == MockStamp("new1")
    assert link2.stamp == MockStamp("old2")  # 更新されない


# ---------------------------------------------------------------------------
# clear_children_stamps テスト
# ---------------------------------------------------------------------------


def test_clear_children_stamps_updates():
    """下方向 clear: child_stamps が最新値に更新される。"""
    parent = MockCrossRootItem("QA-001", child_stamps={"BDD-001": "old"})
    child = MockCrossRootItem("BDD-001", stamp_value="new")
    child_index = {"QA-001": [child]}

    result = clear_children_stamps(parent, child_index)

    assert result is True
    assert parent._data["child_stamps"]["BDD-001"] == "new"
    assert parent._saved is True


def test_clear_children_stamps_adds_new_child():
    """未登録の子が追加される。"""
    parent = MockCrossRootItem("QA-001", child_stamps={})
    child = MockCrossRootItem("BDD-001", stamp_value="abc")
    child_index = {"QA-001": [child]}

    result = clear_children_stamps(parent, child_index)

    assert result is True
    assert parent._data["child_stamps"]["BDD-001"] == "abc"


def test_clear_children_stamps_no_change():
    """stamp 一致 → 更新なし。"""
    parent = MockCrossRootItem("QA-001", child_stamps={"BDD-001": "same"})
    child = MockCrossRootItem("BDD-001", stamp_value="same")
    child_index = {"QA-001": [child]}

    result = clear_children_stamps(parent, child_index)

    assert result is False
    assert parent._saved is False


# ---------------------------------------------------------------------------
# get_item_warnings with cross-root テスト
# ---------------------------------------------------------------------------


def test_get_item_warnings_cross_root_suspect():
    """multi_tree 指定でクロスルート suspect を検出。"""
    parent = MockCrossRootItem("QA-001", stamp_value="new")
    link = MockLinkUID("QA-001", stamp=MockStamp("old"))
    child = MockCrossRootItem("BDD-001", links=[link])

    multi = _make_multi_tree([[parent], [child]])
    w = get_item_warnings(child, multi_tree=multi)

    assert w.has_suspect_links is True
    assert w.suspect_link_targets == ["QA-001"]
    assert w.broken_links == []


def test_get_item_warnings_cross_root_broken_link():
    """multi_tree 指定でリンク切れを warning として報告。"""
    link = MockLinkUID("GONE-001", stamp=MockStamp("x"))
    child = MockCrossRootItem("BDD-001", links=[link])

    multi = _make_multi_tree([[child]])
    w = get_item_warnings(child, multi_tree=multi)

    assert w.has_suspect_links is False
    assert w.broken_links == ["GONE-001"]
    assert w.has_any_warning is True


def test_get_item_warnings_with_child_index():
    """child_index 指定で下方向 suspect を検出。"""
    parent = MockCrossRootItem("QA-001", child_stamps={"BDD-001": "old"})
    child = MockCrossRootItem("BDD-001", stamp_value="new")
    child_index = {"QA-001": [child]}

    multi = _make_multi_tree([[parent], [child]])
    w = get_item_warnings(parent, multi_tree=multi, child_index=child_index)

    assert w.has_suspect_children is True
    assert w.suspect_children == ["BDD-001"]


def test_get_item_warnings_bidirectional_no_loop():
    """双方向チェックが独立して動作し、無限ループにならない。"""
    # QA-001 ← BDD-001 (BDD links to QA)
    link = MockLinkUID("QA-001", stamp=MockStamp("old_qa"))
    parent = MockCrossRootItem(
        "QA-001", stamp_value="new_qa", child_stamps={"BDD-001": "old_bdd"}
    )
    child = MockCrossRootItem("BDD-001", links=[link], stamp_value="new_bdd")

    multi = _make_multi_tree([[parent], [child]])
    child_index = _build_child_index(multi)

    # 子側: 上方向 suspect (QA-001 changed)
    w_child = get_item_warnings(child, multi_tree=multi, child_index=child_index)
    assert w_child.has_suspect_links is True
    assert w_child.suspect_link_targets == ["QA-001"]
    assert w_child.has_suspect_children is False

    # 親側: 下方向 suspect (BDD-001 changed)
    w_parent = get_item_warnings(parent, multi_tree=multi, child_index=child_index)
    assert w_parent.has_suspect_links is False
    assert w_parent.has_suspect_children is True
    assert w_parent.suspect_children == ["BDD-001"]
