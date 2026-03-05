from spec_weaver.adapters.gherkin import get_tag_map


def test_get_tag_map_with_single_file(tmp_path):
    # Setup: Create a feature file
    feature_file = tmp_path / "test.feature"
    feature_file.write_text("""@SPEC-001
Feature: Test Feature
  @SPEC-002
  Scenario: Test Scenario
    Given something
""")
    
    # Execute: call get_tag_map with a single file
    tag_map = get_tag_map(feature_file, tmp_path, prefixes={"SPEC"})
    
    # Verify: tag_map should contain tags from the file
    assert "SPEC-001" in tag_map
    assert "SPEC-002" in tag_map
    assert len(tag_map["SPEC-001"]) == 1
    assert len(tag_map["SPEC-002"]) == 1

def test_get_tag_map_with_directory(tmp_path):
    # Setup: Create a directory with feature files
    feature_dir = tmp_path / "features"
    feature_dir.mkdir()
    (feature_dir / "test1.feature").write_text("@SPEC-001\nFeature: F1\nScenario: S1\nGiven g1")
    (feature_dir / "test2.feature").write_text("@SPEC-002\nFeature: F2\nScenario: S2\nGiven g2")
    
    # Execute: call get_tag_map with a directory
    tag_map = get_tag_map(feature_dir, tmp_path, prefixes={"SPEC"})
    
    # Verify: tag_map should contain tags from both files
    assert "SPEC-001" in tag_map
    assert "SPEC-002" in tag_map
