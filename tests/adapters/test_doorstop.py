from unittest.mock import patch, MagicMock
from spec_weaver.adapters.doorstop import get_specs, get_item_warnings, is_suspect, ItemWarnings, MultiTree


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
