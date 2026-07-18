"""Standard LangChain unit tests for the Bidda tool.

These run fully offline: they check construction, the args schema, and the
tool-call interface without contacting the Bidda API.
"""

from typing import Type

from langchain_bidda import BiddaComplianceTool
from langchain_tests.unit_tests import ToolsUnitTests


class TestBiddaComplianceToolUnit(ToolsUnitTests):
    @property
    def tool_constructor(self) -> Type[BiddaComplianceTool]:
        return BiddaComplianceTool

    @property
    def tool_constructor_params(self) -> dict:
        return {}

    @property
    def tool_invoke_params_example(self) -> dict:
        """Example arguments the tool would be invoked with."""
        return {"query": "EU AI Act Article 10"}
