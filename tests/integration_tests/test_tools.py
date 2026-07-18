"""Standard LangChain integration tests for the Bidda tool.

These contact the live Bidda discovery API (no key required), so they need
network access. Run with: pytest tests/integration_tests
"""

from typing import Type

from langchain_bidda import BiddaComplianceTool
from langchain_tests.integration_tests import ToolsIntegrationTests


class TestBiddaComplianceToolIntegration(ToolsIntegrationTests):
    @property
    def tool_constructor(self) -> Type[BiddaComplianceTool]:
        return BiddaComplianceTool

    @property
    def tool_constructor_params(self) -> dict:
        return {}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {"query": "EU AI Act Article 10"}
