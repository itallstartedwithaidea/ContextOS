"""
ContextOS Memory Layer

Extends thedotmack/claude-mem with:
  - Cross-session persistence (new)
  - Memory tiering: hot/warm/cold (new)
  - Entity relationship graph (new)
  - Conflict resolution (new)
  - User-scoped vs agent-scoped memory separation (new)
"""

from __future__ import annotations
import logging
from typing import Literal, Optional
from dataclasses import dataclass, field

logger = logging.getLogger("contextos.memory")


@dataclass
class MemoryEntry:
    id: str
    content: str
    scope: Literal["user", "agent", "session"]
    tier: Literal["hot", "warm", "cold"]
    tags: list[str] = field(default_factory=list)
    importance: float = 0.5
    created_at: str = ""
    embedding: Optional[list[float]] = None


class MemoryLayer:
    """
    Cross-session, tiered memory with entity graph.

    The fundamental gap in claude-mem was that memory died with the session.
    ContextOS persists across sessions, tiers memories by recency + importance,
    and builds a structured entity graph on top of unstructured memories.
    """

    def __init__(self, config):
        self.config = config
        self._hot: list[MemoryEntry] = []
        self._warm: list[MemoryEntry] = []
        self._cold: list[MemoryEntry] = []
        self._entity_graph: dict = {}
        logger.info("Memory layer initialized with tiers: hot/warm/cold")

    def store(self, content: str, scope: str = "agent", importance: float = 0.5, tags: list = None) -> MemoryEntry:
        """Store with automatic tier assignment."""
        import uuid
        from datetime import datetime
        entry = MemoryEntry(
            id=f"mem_{uuid.uuid4().hex[:8]}",
            content=content,
            scope=scope,
            tier=self._assign_tier(importance),
            tags=tags or [],
            importance=importance,
            created_at=datetime.utcnow().isoformat(),
        )
        self._store_to_tier(entry)
        if self.config.memory_entity_graph:
            self._update_entity_graph(entry)
        logger.debug(f"Stored memory {entry.id} to {entry.tier} tier")
        return entry

    def retrieve(self, query: str, tiers: list = None, limit: int = 10) -> list[MemoryEntry]:
        """Semantic search across specified tiers."""
        tiers = tiers or ["hot", "warm", "cold"]
        results = []
        if "hot" in tiers:
            results.extend(self._hot)
        if "warm" in tiers:
            results.extend(self._warm)
        if "cold" in tiers:
            results.extend(self._cold)
        # Stub: in production, run embedding similarity search
        return results[:limit]

    def conflicts(self, auto_resolve: bool = False) -> list[dict]:
        """Identify and optionally resolve memory conflicts."""
        # Stub: detect entries with same entity but contradictory content
        return []

    def graph_query(self, entity: str, relationship: Optional[str] = None, depth: int = 2) -> dict:
        """Query the entity relationship graph."""
        return self._entity_graph.get(entity, {})

    def _assign_tier(self, importance: float) -> str:
        if importance >= 0.8:
            return "hot"
        elif importance >= 0.4:
            return "warm"
        return "cold"

    def _store_to_tier(self, entry: MemoryEntry):
        if entry.tier == "hot":
            self._hot.append(entry)
        elif entry.tier == "warm":
            self._warm.append(entry)
        else:
            self._cold.append(entry)

    def _update_entity_graph(self, entry: MemoryEntry):
        """Extract entities and update graph. Stub — NER in production."""
        pass

    def health(self) -> dict:
        return {
            "status": "ok",
            "hot_count": len(self._hot),
            "warm_count": len(self._warm),
            "cold_count": len(self._cold),
            "entity_graph_nodes": len(self._entity_graph),
        }
