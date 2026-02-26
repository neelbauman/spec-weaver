from unittest.mock import MagicMock
from spec_weaver.cli import _build_hierarchy_tree

def test_build_hierarchy_tree_only_prefixes():
    # Mock Document and Tree structure
    doc_req = MagicMock()
    doc_req.prefix = "REQ"
    
    doc_spec = MagicMock()
    doc_spec.prefix = "SPEC"
    
    node_spec = MagicMock()
    node_spec.document = doc_spec
    node_spec.children = []
    
    node_req = MagicMock()
    node_req.document = doc_req
    node_req.children = [node_spec]
    
    tree = MagicMock()
    tree.document = doc_req # Root
    tree.children = [node_spec]
    
    # Actually _build_hierarchy_tree starts from doorstop_tree
    # Which seems to have a .document and .children in _build_hierarchy_tree logic
    
    result = _build_hierarchy_tree(node_req)
    
    assert "- [**REQ**](requirements.md)" in result
    assert "    - [**SPEC**](specifications.md)" in result
    # Ensure items are NOT there
    assert "REQ-001" not in result
    assert "SPEC-001" not in result

def test_build_hierarchy_tree_unknown_prefix():
    doc_xyz = MagicMock()
    doc_xyz.prefix = "XYZ"
    
    node_xyz = MagicMock()
    node_xyz.document = doc_xyz
    node_xyz.children = []
    
    result = _build_hierarchy_tree(node_xyz)
    
    # Link should not be there for unknown prefix, just bold
    assert "- **XYZ**" in result
    assert "](xyz.md)" not in result
