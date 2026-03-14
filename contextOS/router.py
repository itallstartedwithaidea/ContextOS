"""
ContextOS Retrieval Router

Churn-aware routing that selects retrieval strategy per data source
based on how fast the underlying data changes.

The insight: the reason coding agents abandoned RAG for grep isn't
philosophical — it's that re-indexing on every branch checkout kills
developer experience. The reason enterprise knowledge bases still use
RAG is that legal docs don't change every 5 minutes.

The real framework isn't "structured vs. unstructured" — it's
data churn rate vs. indexing cost.

This router makes that framework operational.

Origin: Derived from analysis of the "Is RAG Dead?" debate (Cole Medin,
March 2026) and commenter insights about the conflation of RAG with
semantic search. Extended with the observation that local embedding
models + event-driven re-indexing collapse the cost barrier that
originally forced coding agents toward grep-only.
"""

from __future__ import annotations
import logging
import time
from typing import Any, Literal, Optional
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger("contextos.router")


# ---------------------------------------------------------------------------
# Data Source Registry
# ---------------------------------------------------------------------------

@dataclass
class DataSourceProfile:
    """
    Every MCP server self-declares its data profile.
    This is the foundation the router routes against.
    """
    name: str
    mcp_server: str

    # Churn classification
    churn_class: Literal["live", "warm", "cold"] = "warm"
    churn_signal: Optional[str] = None  # event that indicates new data (e.g. "api_pull", "webhook", "cron")

    # Index strategy
    index_strategy: Literal["none", "bm25", "vector", "hybrid"] = "none"
    embedding_model: Optional[str] = None  # tracks which model created the index
    embedding_model_version: Optional[str] = None

    # Freshness
    freshness_threshold_seconds: int = 3600  # how stale before fallback to live pull
    last_indexed_at: Optional[str] = None
    last_data_change_at: Optional[str] = None

    # Schema
    schema_fingerprint: Optional[str] = None  # detects when data shape changes

    # Learned overrides (from feedback loop)
    learned_churn_class: Optional[Literal["live", "warm", "cold"]] = None
    feedback_score: float = 0.5  # how useful this source's results have been (0-1)
    total_retrievals: int = 0
    total_used_in_output: int = 0

    @property
    def effective_churn_class(self) -> str:
        """Use learned class if available, else declared."""
        return self.learned_churn_class or self.churn_class

    @property
    def utilization_rate(self) -> float:
        """What fraction of retrievals from this source actually got used."""
        if self.total_retrievals == 0:
            return 0.0
        return self.total_used_in_output / self.total_retrievals


@dataclass
class IndexHealth:
    """Health status of a source's index."""
    source_name: str
    index_exists: bool = False
    index_fresh: bool = False
    index_age_seconds: int = 0
    model_match: bool = True  # embedding model matches current active model
    schema_match: bool = True  # data schema hasn't changed since indexing
    status: Literal["healthy", "stale", "corrupted", "rebuilding", "missing"] = "missing"
    last_check: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class RoutingDecision:
    """The router's decision for a single retrieval request."""
    source: str
    strategy: Literal["live_pull", "bm25", "vector", "hybrid"]
    reason: str
    fallback_strategy: Optional[str] = None
    index_health: Optional[IndexHealth] = None
    confidence: float = 0.8


# ---------------------------------------------------------------------------
# Retrieval Router
# ---------------------------------------------------------------------------

class RetrievalRouter:
    """
    Churn-aware retrieval router.

    Before any retrieval hits a data source, the router asks:
    1. What data source is being targeted?
    2. What's the registered churn class of that source?
    3. Is the current index within its freshness window?

    Then routes to the right strategy:
    - Live: high churn → direct API call, no index
    - Warm: medium churn → use index if fresh, fall back to live if stale
    - Cold: low churn → always use index, re-index on schedule

    The industry default is one retrieval strategy for everything.
    This makes every retrieval churn-aware.
    """

    def __init__(self, config):
        self.config = config
        self._registry: dict[str, DataSourceProfile] = {}
        self._index_health: dict[str, IndexHealth] = {}
        self._routing_log: list[dict] = []
        logger.info("Retrieval router initialized.")

    # -------------------------------------------------------------------
    # Source Registration
    # -------------------------------------------------------------------

    def register_source(self, profile: DataSourceProfile):
        """Register a data source with its churn profile."""
        self._registry[profile.name] = profile
        self._index_health[profile.name] = IndexHealth(
            source_name=profile.name,
            status="missing" if profile.index_strategy != "none" else "healthy",
        )
        logger.info(
            f"Source registered: {profile.name} | "
            f"churn={profile.churn_class} | "
            f"index={profile.index_strategy}"
        )

    def get_source(self, name: str) -> Optional[DataSourceProfile]:
        return self._registry.get(name)

    def list_sources(self) -> list[DataSourceProfile]:
        return list(self._registry.values())

    # -------------------------------------------------------------------
    # Routing
    # -------------------------------------------------------------------

    def route(self, query: str, target_source: Optional[str] = None) -> list[RoutingDecision]:
        """
        Route a retrieval request to the right strategy per source.

        If target_source is specified, routes for that source only.
        If None, routes across all registered sources.
        """
        sources = [self._registry[target_source]] if target_source and target_source in self._registry \
            else list(self._registry.values())

        decisions = []
        for source in sources:
            decision = self._route_single(query, source)
            decisions.append(decision)
            self._log_routing(query, decision)

        return decisions

    def _route_single(self, query: str, source: DataSourceProfile) -> RoutingDecision:
        """Route decision for a single source."""
        health = self._check_index_health(source)
        churn = source.effective_churn_class

        # Tier 1: Live — always direct pull
        if churn == "live":
            return RoutingDecision(
                source=source.name,
                strategy="live_pull",
                reason="Live churn class — data changes too fast for indexing",
                index_health=health,
                confidence=0.95,
            )

        # Tier 3: Cold — always use index (if healthy)
        if churn == "cold":
            if health.status == "healthy" and health.index_fresh and health.model_match:
                strategy = source.index_strategy if source.index_strategy != "none" else "vector"
                return RoutingDecision(
                    source=source.name,
                    strategy=strategy,
                    reason="Cold churn class — stable data, index is healthy",
                    index_health=health,
                    confidence=0.9,
                )
            else:
                return RoutingDecision(
                    source=source.name,
                    strategy="live_pull",
                    fallback_strategy=source.index_strategy,
                    reason=f"Cold source but index unhealthy: {health.status}",
                    index_health=health,
                    confidence=0.6,
                )

        # Tier 2: Warm — use index if fresh, fallback to live
        if health.status == "healthy" and health.index_fresh and health.model_match and health.schema_match:
            strategy = source.index_strategy if source.index_strategy != "none" else "bm25"
            return RoutingDecision(
                source=source.name,
                strategy=strategy,
                reason="Warm churn class — index is within freshness window",
                index_health=health,
                confidence=0.8,
            )
        else:
            return RoutingDecision(
                source=source.name,
                strategy="live_pull",
                fallback_strategy=source.index_strategy,
                reason=f"Warm source, index not fresh (age={health.index_age_seconds}s, "
                       f"threshold={source.freshness_threshold_seconds}s)",
                index_health=health,
                confidence=0.7,
            )

    # -------------------------------------------------------------------
    # Index Health
    # -------------------------------------------------------------------

    def _check_index_health(self, source: DataSourceProfile) -> IndexHealth:
        """Check the current health of a source's index."""
        health = self._index_health.get(source.name, IndexHealth(source_name=source.name))

        if source.index_strategy == "none":
            health.status = "healthy"  # no index needed
            return health

        # Check freshness
        if source.last_indexed_at:
            indexed_at = datetime.fromisoformat(source.last_indexed_at)
            age = (datetime.utcnow() - indexed_at).total_seconds()
            health.index_age_seconds = int(age)
            health.index_fresh = age < source.freshness_threshold_seconds
            health.index_exists = True
        else:
            health.index_exists = False
            health.index_fresh = False

        # Check embedding model match
        if source.embedding_model and source.embedding_model_version:
            active_model = self.config.active_embedding_model if hasattr(self.config, 'active_embedding_model') else None
            active_version = self.config.active_embedding_model_version if hasattr(self.config, 'active_embedding_model_version') else None
            health.model_match = (
                source.embedding_model == active_model and
                source.embedding_model_version == active_version
            ) if active_model else True

        # Determine status
        if not health.index_exists:
            health.status = "missing"
        elif not health.model_match:
            health.status = "corrupted"  # model drift — index is silently invalid
        elif not health.schema_match:
            health.status = "corrupted"  # data shape changed
        elif not health.index_fresh:
            health.status = "stale"
        else:
            health.status = "healthy"

        health.last_check = datetime.utcnow().isoformat()
        self._index_health[source.name] = health
        return health

    def get_all_health(self) -> dict[str, IndexHealth]:
        """Health check all registered sources."""
        for source in self._registry.values():
            self._check_index_health(source)
        return dict(self._index_health)

    # -------------------------------------------------------------------
    # Feedback Loop — Churn Class Learning
    # -------------------------------------------------------------------

    def record_retrieval_feedback(
        self,
        source_name: str,
        strategy_used: str,
        result_used_in_output: bool,
        staleness_detected: bool = False,
    ):
        """
        Record whether a retrieval was useful.
        Over time, this reclassifies churn classes empirically.
        """
        source = self._registry.get(source_name)
        if not source:
            return

        source.total_retrievals += 1
        if result_used_in_output:
            source.total_used_in_output += 1

        # Reclassify if we see a pattern
        if staleness_detected and source.total_retrievals > 10:
            stale_rate = 1.0 - source.utilization_rate
            if stale_rate > 0.5 and source.churn_class != "live":
                old_class = source.effective_churn_class
                source.learned_churn_class = "live"
                logger.warning(
                    f"Churn reclassification: {source_name} "
                    f"{old_class} → live (stale_rate={stale_rate:.2f})"
                )
            elif stale_rate < 0.1 and source.churn_class != "cold":
                old_class = source.effective_churn_class
                source.learned_churn_class = "cold"
                logger.info(
                    f"Churn reclassification: {source_name} "
                    f"{old_class} → cold (stale_rate={stale_rate:.2f})"
                )

    # -------------------------------------------------------------------
    # Data Change Events — The Indexing Trigger
    # -------------------------------------------------------------------

    def on_data_change(self, source_name: str, event_type: str = "write"):
        """
        Called when an MCP server pushes new data.
        This is the event-driven re-indexing trigger.

        The MCP data flow IS the indexing trigger.
        No cron jobs. No manual refresh. The write event fires,
        the index rebuilds.
        """
        source = self._registry.get(source_name)
        if not source:
            return

        source.last_data_change_at = datetime.utcnow().isoformat()

        # For warm/cold sources with indexes, signal that re-index is needed
        if source.index_strategy != "none":
            health = self._index_health.get(source_name)
            if health:
                health.index_fresh = False
                health.status = "stale"
                logger.info(
                    f"Data change event for {source_name} — "
                    f"index marked stale, re-index queued"
                )
                # In production: emit event to IndexLifecycleManager
                return {"action": "reindex", "source": source_name, "priority": "normal"}

        return {"action": "none", "source": source_name}

    # -------------------------------------------------------------------
    # Logging
    # -------------------------------------------------------------------

    def _log_routing(self, query: str, decision: RoutingDecision):
        self._routing_log.append({
            "query": query[:100],
            "source": decision.source,
            "strategy": decision.strategy,
            "confidence": decision.confidence,
            "reason": decision.reason,
            "timestamp": datetime.utcnow().isoformat(),
        })

    # -------------------------------------------------------------------
    # Health
    # -------------------------------------------------------------------

    def health(self) -> dict:
        source_health = self.get_all_health()
        return {
            "status": "ok",
            "sources_registered": len(self._registry),
            "sources_healthy": sum(1 for h in source_health.values() if h.status == "healthy"),
            "sources_stale": sum(1 for h in source_health.values() if h.status == "stale"),
            "sources_corrupted": sum(1 for h in source_health.values() if h.status == "corrupted"),
            "total_routing_decisions": len(self._routing_log),
        }
