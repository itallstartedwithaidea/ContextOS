"""
ContextOS — The unified context intelligence layer for AI agents.

One pip install. Every capability. Nothing missing.

v0.2.0 — The Cognition Update:
  The industry builds: retrieve → generate
  ContextOS builds: retrieve → THINK → generate

  New layers:
  - CognitionLayer: six cognitive primitives for reasoning between
    retrieval and output (active forgetting, depth calibration,
    synthesis detection, unknown-unknown sensing, productive
    contradiction, context-dependent gravity)
  - RetrievalRouter: churn-aware routing per data source
  - IndexLifecycleManager: self-healing, event-driven re-indexing

Built with respect for:
  - modelcontextprotocol/servers (80.5k stars)
  - infiniflow/ragflow (74.4k stars)
  - dair-ai/Prompt-Engineering-Guide (71.3k stars)
  - upstash/context7 (48.2k stars)
  - thedotmack/claude-mem (33.5k stars)
  - ComposioHQ/composio (27.3k stars)
  - gsd-build/get-shit-done (26.5k stars)
"""

__version__ = "0.2.0"
__author__ = "John Williams / IASAWI"
__license__ = "MIT"

from .core import ContextOS
from .memory import MemoryLayer
from .retrieval import RetrievalLayer
from .tools import ToolLayer
from .planning import PlanningLayer
from .orchestration import OrchestrationCore
from .cognition import CognitionLayer
from .router import RetrievalRouter
from .indexer import IndexLifecycleManager

__all__ = [
    "ContextOS",
    "MemoryLayer",
    "RetrievalLayer",
    "ToolLayer",
    "PlanningLayer",
    "OrchestrationCore",
    "CognitionLayer",
    "RetrievalRouter",
    "IndexLifecycleManager",
]
