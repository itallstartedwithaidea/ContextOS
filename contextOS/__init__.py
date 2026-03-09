"""
ContextOS — The unified context intelligence layer for AI agents.

One pip install. Every capability. Nothing missing.

Built with respect for:
  - modelcontextprotocol/servers (80.5k ⭐)
  - infiniflow/ragflow (74.4k ⭐)
  - dair-ai/Prompt-Engineering-Guide (71.3k ⭐)
  - upstash/context7 (48.2k ⭐)
  - thedotmack/claude-mem (33.5k ⭐)
  - ComposioHQ/composio (27.3k ⭐)
  - gsd-build/get-shit-done (26.5k ⭐)
"""

__version__ = "0.1.0"
__author__ = "John Williams / IASAWI"
__license__ = "MIT"

from .core import ContextOS
from .memory import MemoryLayer
from .retrieval import RetrievalLayer
from .tools import ToolLayer
from .planning import PlanningLayer
from .orchestration import OrchestrationCore

__all__ = [
    "ContextOS",
    "MemoryLayer",
    "RetrievalLayer",
    "ToolLayer",
    "PlanningLayer",
    "OrchestrationCore",
]
