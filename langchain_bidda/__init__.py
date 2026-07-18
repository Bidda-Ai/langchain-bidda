"""langchain-bidda: Bidda source-verified compliance intelligence for LangChain."""

from importlib import metadata

from langchain_bidda.tools import BiddaComplianceTool, BiddaSearchInput

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    # Package is not installed (e.g. running from a source checkout).
    __version__ = ""

__all__ = ["BiddaComplianceTool", "BiddaSearchInput", "__version__"]
