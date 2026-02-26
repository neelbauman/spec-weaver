from unittest.mock import patch, MagicMock
from spec_weaver.doorstop import get_specs

class MockDoorstopItem:
    def __init__(self, uid, prefix, active=True, testable=True):
        self.uid = uid
        self.document = MagicMock()
        self.document.prefix = prefix
        self.active = active
        self.testable = testable

@patch("spec_weaver.doorstop.doorstop.build")
@patch("spec_weaver.doorstop.os.chdir") # ディレクトリ移動をモックしてテスト環境を保護
def test_get_specs_filtering(mock_chdir, mock_build, tmp_path):
    # Doorstopのツリーをシミュレート
    mock_tree = [
        MockDoorstopItem("SPEC-001", "SPEC", active=True, testable=True),     # 抽出されるべき
        MockDoorstopItem("SPEC-002", "SPEC", active=False, testable=True),    # 削除済み(active=False)なので除外
        MockDoorstopItem("SPEC-003", "SPEC", active=True, testable=False),    # テスト不要(testable=False)なので除外
        MockDoorstopItem("REQ-001", "REQ", active=True, testable=True),       # プレフィックス違いなので除外
    ]
    mock_build.return_value = mock_tree

    # 実行と検証
    specs = get_specs(repo_root=tmp_path, prefix="SPEC")
    
    assert specs == {"SPEC-001"}
