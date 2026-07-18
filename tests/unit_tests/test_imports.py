"""Import-surface tests. Run with: pytest tests/unit_tests"""

from langchain_bidda import BiddaComplianceTool, BiddaSearchInput


def test_public_api() -> None:
    assert BiddaComplianceTool is not None
    assert BiddaSearchInput is not None


def test_tool_metadata() -> None:
    tool = BiddaComplianceTool()
    assert tool.name == "bidda_compliance"
    assert isinstance(tool.description, str) and tool.description
    # The args schema exposes exactly one field: query.
    assert "query" in tool.args_schema.model_fields
