# langchain-bidda

Source-verified regulatory and compliance intelligence for LangChain agents, from the [Bidda](https://bidda.com) registry.

`langchain-bidda` gives a LangChain agent a tool that looks up what a regulation, law, or standard requires and returns a plain summary traced to a primary legal source with a content hash. Each answer points back to the primary instrument, so an agent can cite what it relied on instead of relying on the model's own recall.

This is reference intelligence, not legal advice. The reader draws the legal conclusion.

## Installation

```bash
pip install -U langchain-bidda
```

## Tools

### `BiddaComplianceTool`

Looks up source-verified compliance intelligence across the Bidda registry (10,000+ obligations across 39 regulated pillars, including the EU AI Act, GDPR, DORA, NIS2, HIPAA, Basel III, and the MITRE ATT&CK / ATLAS / D3FEND / CAPEC families). Uses the free discovery tier, so no API key is required.

```python
from langchain_bidda import BiddaComplianceTool

tool = BiddaComplianceTool()

print(tool.invoke({"query": "EU AI Act Article 10"}))
```

Example output:

```
Regulation: Regulation (EU) 2024/1689 - Article 10: Data and data governance
Pillar: AI Governance & Law
Summary: High-risk AI systems trained on data must meet data governance and management practices ...
Node ID: eu-ai-act-article-10-data-governance-training
Source (full node): https://bidda.com/intelligence/eu-ai-act-article-10-data-governance-training
```

## Use inside an agent

```python
from langchain.chat_models import init_chat_model
from langchain_bidda import BiddaComplianceTool

llm = init_chat_model("gpt-4o-mini", model_provider="openai")
agent = llm.bind_tools([BiddaComplianceTool()])

agent.invoke("What does the EU AI Act require for training data governance?")
```

## Configuration

| Field | Default | Purpose |
| --- | --- | --- |
| `pillar` | `None` | Restrict results to one pillar slug, e.g. `"cybersecurity"` or `"ai-governance"`. |
| `max_results` | `4` | How many related node ids to surface after the top match. |
| `skyfire_token` / `base_tx_hash` | `None` | Optional credentials for callers who also pull full (gated) node payloads. Not needed for discovery search. |

## Links

- Bidda developer docs: https://bidda.com/developers
- API and MCP server: https://bidda.com/developers
- Underlying SDK: [`bidda-shield`](https://pypi.org/project/bidda-shield/)

## License

MIT
