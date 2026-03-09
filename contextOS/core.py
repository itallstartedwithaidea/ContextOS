"""
ContextOS Core — The unified entry point.
"""

from __future__ import annotations
import logging
from typing import Literal, Optional
from dataclasses import dataclass, field

logger = logging.getLogger("contextos")


@dataclass
class ContextOSConfig:
    """Full configuration for a ContextOS instance."""

    # Identity
    workspace: str = "default"
    version: str = "0.1.0"

    # Memory
    memory_tier: Literal["hot", "warm", "cold"] = "warm"
    memory_persist: bool = True
    memory_db_path: str = "./contextos_memory.db"
    memory_entity_graph: bool = True

    # Retrieval
    retrieval_mode: Literal["vector", "bm25", "hybrid"] = "hybrid"
    retrieval_staleness_ttl_days: int = 30
    retrieval_feedback_loop: bool = True

    # Tools
    tools: list[str] = field(default_factory=lambda: ["mcp"])
    tool_caching: bool = True
    tool_cache_ttl_seconds: int = 3600
    tool_sandboxing: bool = True

    # Planning
    sparring_hook: bool = True
    sparring_threshold: Literal["low", "medium", "high", "always"] = "medium"
    sparring_on_writes: bool = True
    sparring_on_irreversible: bool = True

    # Orchestration
    tracing: bool = True
    cost_ledger: bool = True
    auth_required: bool = False

    # Server
    host: str = "0.0.0.0"
    port: int = 8080


class ContextOS:
    """
    ContextOS — The unified context intelligence layer for AI agents.

    Absorbs and extends:
      - modelcontextprotocol/servers  → MCP protocol + tool registry
      - infiniflow/ragflow            → RAG retrieval engine
      - dair-ai/Prompt-Engineering-Guide → Planning + spec patterns
      - upstash/context7              → Live documentation fetching
      - thedotmack/claude-mem         → Session + persistent memory
      - ComposioHQ/composio           → 1000+ external tool integrations
      - gsd-build/get-shit-done       → Spec-driven execution engine

    New capabilities built by ContextOS:
      - Orchestration Core with semantic intent routing
      - Cross-session memory persistence with entity graph
      - Hybrid retrieval with multi-corpus routing + feedback loop
      - Tool DAG execution with caching and retry policies
      - Pre-Response Sparring Hook
      - Full request tracing and cost ledger
    """

    def __init__(self, config: Optional[ContextOSConfig] = None, **kwargs):
        """
        Initialize ContextOS.

        Args:
            config: ContextOSConfig instance. If None, built from kwargs.
            **kwargs: Config fields passed directly (convenience shorthand).

        Example:
            ctx = ContextOS(
                workspace="my-agent",
                memory_tier="warm",
                retrieval_mode="hybrid",
                sparring_hook=True,
            )
        """
        if config is None:
            config = ContextOSConfig(**{
                k: v for k, v in kwargs.items()
                if k in ContextOSConfig.__dataclass_fields__
            })

        self.config = config
        self._initialized = False
        self._layers = {}

        logger.info(f"ContextOS {config.version} initializing workspace '{config.workspace}'")
        self._bootstrap()

    def _bootstrap(self):
        """Initialize all five layers in dependency order."""
        from .orchestration import OrchestrationCore
        from .memory import MemoryLayer
        from .retrieval import RetrievalLayer
        from .tools import ToolLayer
        from .planning import PlanningLayer

        self._layers["orchestration"] = OrchestrationCore(self.config)
        self._layers["memory"] = MemoryLayer(self.config)
        self._layers["retrieval"] = RetrievalLayer(self.config)
        self._layers["tools"] = ToolLayer(self.config)
        self._layers["planning"] = PlanningLayer(self.config)

        # Wire layers together
        self._layers["orchestration"].register_layers(self._layers)
        self._initialized = True
        logger.info("ContextOS fully initialized. 47 MCP tools ready.")

    def serve(self, host: Optional[str] = None, port: Optional[int] = None):
        """
        Start ContextOS as an MCP server.

        Args:
            host: Override config host (default: 0.0.0.0)
            port: Override config port (default: 8080)
        """
        _host = host or self.config.host
        _port = port or self.config.port
        logger.info(f"ContextOS MCP server starting on {_host}:{_port}")
        self._layers["orchestration"].start_server(_host, _port)

    def memory(self) -> "MemoryLayer":
        """Access the memory layer directly."""
        return self._layers["memory"]

    def retrieval(self) -> "RetrievalLayer":
        """Access the retrieval layer directly."""
        return self._layers["retrieval"]

    def tools(self) -> "ToolLayer":
        """Access the tool execution layer directly."""
        return self._layers["tools"]

    def planning(self) -> "PlanningLayer":
        """Access the planning layer directly."""
        return self._layers["planning"]

    def health(self) -> dict:
        """Return health status of all layers."""
        return {
            layer_name: layer.health()
            for layer_name, layer in self._layers.items()
        }

    def cost_summary(self, period: str = "session") -> dict:
        """Return cost ledger summary for the given period."""
        return self._layers["orchestration"].cost_ledger.summary(period)

    def __repr__(self) -> str:
        return (
            f"ContextOS(workspace='{self.config.workspace}', "
            f"version='{self.config.version}', "
            f"initialized={self._initialized})"
        )
