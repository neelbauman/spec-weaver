import os
import pytest
import doorstop
import subprocess
from pathlib import Path
from typer.testing import CliRunner
from spec_weaver.cli import app

runner = CliRunner()

@pytest.fixture
def repo_root(tmp_path):
    """Doorstopプロジェクトの初期化を行うフィクスチャ"""
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        # Git リポジトリの初期化
        subprocess.run(["git", "init"], check=True, capture_output=True)
        
        # SPEC ドキュメントの作成
        subprocess.run(["doorstop", "create", "SPEC", "specs"], check=True, capture_output=True)
        
        # アイテムの追加
        subprocess.run(["doorstop", "add", "SPEC"], check=True, capture_output=True)
        
        tree = doorstop.build(root=str(tmp_path))
        item = tree.find_item("SPEC1") or tree.find_item("SPEC-001") or tree.find_item("SPEC-1")
        if not item:
            # 万が一見つからない場合は最初の一件を取得
            doc = tree.find_document("SPEC")
            item = list(doc.items)[0]
        
        item.header = "Test Specification"
        item.text = "This is a test SPEC."
        item.save()
        
        yield tmp_path
    finally:
        os.chdir(original_cwd)

def test_gherkin_fingerprint_audit_and_review(repo_root):
    tree = doorstop.build(root=str(repo_root))
    doc = tree.find_document("SPEC")
    item = list(doc.items)[0]
    spec_id = str(item.uid)
    
    # feature ファイルの作成
    feature_dir = repo_root / "features"
    feature_dir.mkdir()
    feature_file = feature_dir / "test.feature"
    feature_file.write_text(f"""Feature: Test Feature
  @{spec_id}
  Scenario: Test Scenario
    Given a test condition
    When I do something
    Then something happens
""", encoding="utf-8")

    # 1. 最初は test_fingerprint がないので Test Unreviewed になるはず
    result = runner.invoke(app, ["audit", str(feature_dir), "--repo-root", str(repo_root)])
    assert result.exit_code == 1
    assert "Test Unreviewed" in result.stdout

    # 2. review コマンドで更新
    result = runner.invoke(app, ["review", spec_id, "-f", str(feature_dir), "-r", str(repo_root)])
    assert result.exit_code == 0
    assert f"{spec_id} のフィンガープリントを更新しました" in result.stdout

    # 3. audit が通るようになるか確認
    # 注意: アイテム自体が unreviewed だと失敗するので、あらかじめ doorstop review しておく
    subprocess.run(["doorstop", "review", spec_id], cwd=str(repo_root), check=True, capture_output=True)

    result = runner.invoke(app, ["audit", str(feature_dir), "--repo-root", str(repo_root)])
    if result.exit_code != 0:
        print(result.stdout)
    assert result.exit_code == 0
    assert "完璧です" in result.stdout

    # 4. feature を変更して audit が再度失敗するか確認
    feature_file.write_text(f"""Feature: Test Feature
  @{spec_id}
  Scenario: Test Scenario Modified
    Given a test condition
    When I do something
    Then something happens
""", encoding="utf-8")

    result = runner.invoke(app, ["audit", str(feature_dir), "--repo-root", str(repo_root)])
    assert result.exit_code == 1
    assert "Test Unreviewed" in result.stdout

    # 5. status コマンドでの表示確認
    result = runner.invoke(app, ["status", "-f", str(feature_dir), "-r", str(repo_root)])
    assert result.exit_code == 0
    assert "test-unreviewed" in result.stdout

def test_spec_change_makes_it_unreviewed_and_suspect_in_status(repo_root):
    tree = doorstop.build(root=str(repo_root))
    doc = tree.find_document("SPEC")
    item = list(doc.items)[0]
    spec_id = str(item.uid)

    feature_dir = repo_root / "features"
    feature_dir.mkdir(exist_ok=True)
    (feature_dir / "test.feature").write_text(f"@{spec_id}\nFeature: T\nScenario: S\n  Given G", encoding="utf-8")
    
    # 初回 review
    runner.invoke(app, ["review", spec_id, "-f", str(feature_dir), "-r", str(repo_root)])
    
    # Doorstop 本体で review 済みとする
    tree = doorstop.build(root=str(repo_root))
    item = tree.find_item(spec_id)
    item.review()
    item.save()
    
    # status で reviewed となっていることを確認
    result = runner.invoke(app, ["status", "-f", str(feature_dir), "-r", str(repo_root)])
    assert "reviewed" in result.stdout
    
    # SPEC の中身を変更
    item.text = "Updated text"
    item.save()
    
    # status で test-suspect となっていることを確認
    result = runner.invoke(app, ["status", "-f", str(feature_dir), "-r", str(repo_root)])
    assert "test-suspect" in result.stdout
