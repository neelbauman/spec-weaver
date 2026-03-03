import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

from spec_weaver.services.trace_service import TraceService, TraceData

@pytest.fixture
def mock_repo_root():
    return Path("/mock/repo")

@pytest.fixture
def mock_feature_dir():
    return Path("/mock/repo/features")

@pytest.fixture
def trace_service():
    return TraceService()

def _make_mock_item(uid: str, links: list | None = None):
    item = MagicMock()
    item.uid = uid
    item.links = links or []
    return item

@patch("spec_weaver.services.trace_service.get_item_map")
@patch("spec_weaver.services.trace_service.get_all_prefixes")
@patch("spec_weaver.services.trace_service.get_tag_map")
@patch("spec_weaver.services.trace_service.get_spec_fingerprints")
@patch("spec_weaver.services.trace_service.compute_review_state")
@patch("spec_weaver.services.trace_service.AuditService")
@patch("spec_weaver.services.trace_service.ImplScanner")
@patch("spec_weaver.services.trace_service.get_ref_files")
def test_prepare_trace_data_full(
    mock_get_ref_files,
    mock_impl_scanner_cls,
    mock_audit_service_cls,
    mock_compute_review_state,
    mock_get_spec_fingerprints,
    mock_get_tag_map,
    mock_get_all_prefixes,
    mock_get_item_map,
    trace_service,
    mock_repo_root,
    mock_feature_dir
):
    # Setup mocks
    mock_item_parent = _make_mock_item("REQ-001")
    mock_item_child = _make_mock_item("SPEC-001", links=["REQ-001"])
    mock_get_item_map.return_value = {
        "REQ-001": mock_item_parent,
        "SPEC-001": mock_item_child
    }

    mock_get_all_prefixes.return_value = {"REQ", "SPEC"}
    mock_get_tag_map.return_value = {"SPEC-001": [{"file": "login.feature"}]}
    mock_get_spec_fingerprints.return_value = {}

    mock_review_state = MagicMock()
    mock_compute_review_state.return_value = mock_review_state

    # Setup impl scanner mock
    mock_scanner_instance = MagicMock()
    mock_scanner_instance.scan.return_value = {"SPEC-001": {"src/login.py"}}
    mock_impl_scanner_cls.return_value = mock_scanner_instance

    mock_get_ref_files.return_value = ["docs/design.md"]

    # Execute
    data = trace_service.prepare_trace_data(
        repo_root=mock_repo_root,
        feature_dir=mock_feature_dir,
        show_impl=True,
        extensions=[".py"]
    )

    # Assert
    assert isinstance(data, TraceData)
    assert len(data.all_items_str) == 2
    assert "REQ-001" in data.all_items_str
    
    # Assert child map
    assert data.child_map == {"REQ-001": ["SPEC-001"]}
    
    # Assert tag map
    assert data.tag_map == {"SPEC-001": [{"file": "login.feature"}]}
    
    # Assert review state
    assert data.review_state is mock_review_state

    # Assert impl map
    # "docs/design.md" from get_ref_files + "src/login.py" from annotation map
    assert "SPEC-001" in data.impl_map
    assert data.impl_map["SPEC-001"] == {"src/login.py", "docs/design.md"}


@patch("spec_weaver.services.trace_service.get_item_map")
@patch("spec_weaver.services.trace_service.compute_review_state")
def test_prepare_trace_data_no_feature_dir_no_impl(
    mock_compute_review_state,
    mock_get_item_map,
    trace_service,
    mock_repo_root
):
    mock_item = _make_mock_item("REQ-001")
    mock_get_item_map.return_value = {"REQ-001": mock_item}

    mock_review_state = MagicMock()
    mock_compute_review_state.return_value = mock_review_state

    # Execute
    data = trace_service.prepare_trace_data(
        repo_root=mock_repo_root,
        feature_dir=None,
        show_impl=False,
        extensions=None
    )

    # Assert
    assert data.tag_map == {}
    assert data.impl_map is None
    assert data.review_state is mock_review_state
