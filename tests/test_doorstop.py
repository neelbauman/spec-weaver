from unittest.mock import patch, MagicMock
from spec_weaver.doorstop import get_specs

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
@patch("spec_weaver.doorstop.os.chdir") # ディレクトリ移動をモックしてテスト環境を保護
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

from spec_weaver.doorstop import is_suspect

def test_is_suspect():
    class MockLink:
        def __init__(self, suspect=False):
            self.suspect = suspect

    class MockItem:
        def __init__(self, suspect=False, links=None):
            self.suspect = suspect
            self.links = links or []

    # 1. アイテム自体がsuspect
    item1 = MockItem(suspect=True)
    assert is_suspect(item1) is True

    # 2. リンクのいずれかがsuspect
    item2 = MockItem(links=[MockLink(suspect=False), MockLink(suspect=True)])
    assert is_suspect(item2) is True

    # 3. どちらもsuspectではない
    item3 = MockItem(suspect=False, links=[MockLink(suspect=False)])
    assert is_suspect(item3) is False

    # 4. attribute が無い場合などの安全なフォールバック
    class EmptyItem:
        pass
    assert is_suspect(EmptyItem()) is False
