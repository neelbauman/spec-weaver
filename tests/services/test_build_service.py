from unittest.mock import MagicMock
from spec_weaver.services.build_service import BuildService
from spec_weaver.adapters.doorstop import MultiTree


def _make_tree_node(prefix: str, children=None):
    """MagicMock で doorstop.Tree ノードを模倣するヘルパー。"""
    doc = MagicMock()
    doc.prefix = prefix
    node = MagicMock()
    node.document = doc
    node.children = children or []
    return node


def test_build_hierarchy_tree_only_prefixes():
    node_spec = _make_tree_node("SPEC")
    node_req = _make_tree_node("REQ", children=[node_spec])

    multi_tree = MultiTree([node_req])
    prefix_to_file = {"REQ": "requirements.md", "SPEC": "specifications.md"}

    result = BuildService()._build_hierarchy_tree(multi_tree, prefix_to_file)

    assert "- [**REQ**](requirements.md)" in result
    assert "    - [**SPEC**](specifications.md)" in result
    assert "REQ-001" not in result
    assert "SPEC-001" not in result


def test_build_hierarchy_tree_unknown_prefix():
    node_xyz = _make_tree_node("XYZ")
    multi_tree = MultiTree([node_xyz])

    result = BuildService()._build_hierarchy_tree(multi_tree, {})

    assert "- **XYZ**" in result
    assert "](xyz.md)" not in result


def test_build_hierarchy_tree_multiple_roots():
    """複数ルートを持つ MultiTree が両方レンダリングされる。"""
    node_req = _make_tree_node("REQ")
    node_core = _make_tree_node("CORE")

    multi_tree = MultiTree([node_req, node_core])
    prefix_to_file = {"REQ": "req.md", "CORE": "core.md"}

    result = BuildService()._build_hierarchy_tree(multi_tree, prefix_to_file)

    assert "- [**REQ**](req.md)" in result
    assert "- [**CORE**](core.md)" in result
