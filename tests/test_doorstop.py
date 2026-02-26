from unittest.mock import patch, MagicMock
from spec_weaver.doorstop import get_specs, get_item_warnings, is_suspect, ItemWarnings


class MockDoorstopItem:
    def __init__(self, uid, prefix, active=True, testable=True):
        self.uid = uid
        self.document = MagicMock()
        self.document.prefix = prefix
        self.active = active
        self.testable = testable


class MockDoorstopDocument:
    def __init__(self, items):
        self.items = items

    def __iter__(self):
        return iter(self.items)


@patch("spec_weaver.doorstop.doorstop.build")
@patch("spec_weaver.doorstop.os.chdir")  # ディレクトリ移動をモックしてテスト環境を保護
def test_get_specs_filtering(mock_chdir, mock_build, tmp_path):
    # Doorstopのツリーをシミュレート
    items = [
        MockDoorstopItem("SPEC-001", "SPEC", active=True, testable=True),     # 抽出されるべき
        MockDoorstopItem("SPEC-002", "SPEC", active=False, testable=True),    # 削除済み(active=False)なので除外
        MockDoorstopItem("SPEC-003", "SPEC", active=True, testable=False),    # テスト不要(testable=False)なので除外
        MockDoorstopItem("REQ-001", "REQ", active=True, testable=True),       # プレフィックス違いなので除外
    ]
    mock_build.return_value = [MockDoorstopDocument(items)]

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
