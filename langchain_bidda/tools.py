"""Bidda compliance intelligence tool for LangChain.

Exposes the Bidda registry of source-verified regulatory and compliance
intelligence as a LangChain ``BaseTool`` so an agent can look up what a
regulation requires and cite a primary source, instead of relying on the
model's own recall.

The tool uses the free discovery tier of the Bidda API (no key required).
Full node payloads (deterministic workflow, actionable schema, full
citation list) are available via the Bidda API for authenticated callers.
"""

from __future__ import annotations

from typing import List, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

DEFAULT_MAX_RESULTS = 4


class BiddaSearchInput(BaseModel):
    """Input schema for the Bidda compliance search tool."""

    query: str = Field(
        description=(
            "A regulation name, standard, keyword, technique ID, or compliance "
            "topic to look up. Examples: 'EU AI Act Article 10', "
            "'GDPR data retention', 'HIPAA breach notification', 'DORA', "
            "'MITRE ATLAS prompt injection'."
        )
    )


class BiddaComplianceTool(BaseTool):
    """Look up source-verified regulatory and compliance intelligence from Bidda.

    Each result is traced to a primary legal source with a content hash, so an
    agent can cite what it relied on. This is reference intelligence, not legal
    advice; the reader draws the legal conclusion.

    Setup:
        Install ``langchain-bidda``.

        .. code-block:: bash

            pip install -U langchain-bidda

    Instantiate:
        .. code-block:: python

            from langchain_bidda import BiddaComplianceTool

            tool = BiddaComplianceTool()

    Invoke directly:
        .. code-block:: python

            tool.invoke({"query": "EU AI Act Article 10"})

    Invoke with a tool call (inside an agent):
        .. code-block:: python

            tool.invoke(
                {
                    "args": {"query": "GDPR breach notification deadline"},
                    "id": "1",
                    "name": tool.name,
                    "type": "tool_call",
                }
            )
    """

    name: str = "bidda_compliance"
    description: str = (
        "Look up source-verified regulatory and compliance intelligence for any "
        "law, regulation, or standard. Use this when you need to know what a "
        "regulation requires, which obligations apply to an AI action, data "
        "processing activity, or business operation, or which framework governs a "
        "topic. Returns a plain summary with the issuing pillar and a link to the "
        "primary source. Input: a regulation name, standard, keyword, or topic."
    )
    args_schema: Type[BaseModel] = BiddaSearchInput

    # Optional auth for callers who also want to pull full (gated) node payloads.
    # Not required for discovery-tier search, which this tool uses.
    skyfire_token: Optional[str] = None
    base_tx_hash: Optional[str] = None
    # Optional pillar-slug filter (e.g. "cybersecurity", "ai-governance").
    pillar: Optional[str] = None
    # How many related node ids to surface after the top match.
    max_results: int = DEFAULT_MAX_RESULTS

    def _client(self):
        # Imported lazily so importing this package does not require a network
        # call and unit tests can run without contacting the API.
        from bidda_shield import BiddaShield

        return BiddaShield(
            skyfire_token=self.skyfire_token, base_tx_hash=self.base_tx_hash
        )

    def _format(self, results: List[dict]) -> str:
        if not results:
            return (
                "No compliance nodes found for that query. Try a broader term, "
                "or a specific instrument name such as 'EU AI Act' or 'GDPR'."
            )
        top = results[0]
        lines = [
            f"Regulation: {top.get('title', 'Unknown')}",
            f"Pillar: {top.get('domain', 'Unknown')}",
            f"Summary: {top.get('bluf', 'No summary available.')}",
            f"Node ID: {top.get('node_id', '')}",
            f"Source (full node): https://bidda.com/intelligence/{top.get('node_id', '')}",
        ]
        related = [
            r.get("node_id", "")
            for r in results[1 : self.max_results]
            if r.get("node_id")
        ]
        if related:
            lines.append("Related nodes: " + ", ".join(related))
        return "\n".join(lines)

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        results = self._client().search_nodes(query, pillar=self.pillar)
        return self._format(results)

    async def _arun(
        self,
        query: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        # The underlying SDK call is synchronous; delegate to the sync path.
        return self._run(query)


__all__ = ["BiddaComplianceTool", "BiddaSearchInput"]
