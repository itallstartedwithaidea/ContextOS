"""
ContextOS Index Lifecycle Manager

Self-healing index infrastructure that rebuilds automatically
when data changes, detects embedding model drift, and degrades
gracefully when indexes are unhealthy.

The old constraint: Re-embedding is expensive and slow.
What changed: Local embedding models run on commodity hardware.
BM25 indexes rebuild in seconds.

This makes the retrieval router's decisions operational.
The router decides WHAT strategy to use.
The lifecycle manager ensures the indexes are ready.
"""

from __future__ import annotations
import logging
import time
import hashlib
from typing import Any, Literal, Optional
from dataclasses import dataclass, field
from datetime import datetime
from .router import DataSourceProfile, IndexHealth, RetrievalRouter

logger = logging.getLogger("contextos.indexer")


@dataclass
class IndexJob:
    """A single index build/rebuild job."""
    id: str
    source_name: str
    job_type: Literal["full_build", "incremental", "rebuild_model_change", "rebuild_schema_change"]
    strategy: Literal["bm25", "vector", "hybrid"]
    status: Literal["queued", "running", "completed", "failed"] = "queued"
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    completed_at: Optional[str] = None
    documents_processed: int = 0
    error: Optional[str] = None
    duration_ms: int = 0
    trigger: str = ""  # what caused this job: "data_change", "model_change", "schema_change", "manual", "heartbeat"


@dataclass
class CircuitBreakerState:
    """
    Circuit breaker for index operations per source.
    If re-indexing fails repeatedly, stop trying and degrade to live pull.
    """
    source_name: str
    consecutive_failures: int = 0
    state: Literal["closed", "open", "half_open"] = "closed"  # closed = normal, open = tripped
    last_failure_at: Optional[str] = None
    cooldown_seconds: int = 300  # wait before retrying after trip
    failure_threshold: int = 3  # trips after N consecutive failures

    @property
    def is_tripped(self) -> bool:
        return self.state == "open"

    def record_failure(self):
        self.consecutive_failures += 1
        self.last_failure_at = datetime.utcnow().isoformat()
        if self.consecutive_failures >= self.failure_threshold:
            self.state = "open"
            logger.warning(f"Circuit breaker TRIPPED for {self.source_name} after {self.consecutive_failures} failures")

    def record_success(self):
        self.consecutive_failures = 0
        self.state = "closed"

    def can_retry(self) -> bool:
        if self.state == "closed":
            return True
        if self.state == "open" and self.last_failure_at:
            failed_at = datetime.fromisoformat(self.last_failure_at)
            elapsed = (datetime.utcnow() - failed_at).total_seconds()
            if elapsed > self.cooldown_seconds:
                self.state = "half_open"
                return True
        return self.state == "half_open"


class IndexLifecycleManager:
    """
    Manages the full lifecycle of indexes across all data sources.

    Responsibilities:
    1. Event-driven re-indexing: MCP data flow triggers index rebuilds
    2. Heartbeat freshness checks: catch sources that changed without events
    3. Embedding model drift detection: auto-rebuild when model version changes
    4. Schema change detection: quarantine and rebuild when data shape changes
    5. Circuit breakers: degrade gracefully when indexing fails
    6. Self-healing: automatically recover from corrupted or missing indexes
    """

    def __init__(self, config, router: RetrievalRouter):
        self.config = config
        self.router = router
        self._job_queue: list[IndexJob] = []
        self._job_history: list[IndexJob] = []
        self._circuit_breakers: dict[str, CircuitBreakerState] = {}
        self._active_model: str = getattr(config, 'active_embedding_model', 'all-MiniLM-L6-v2')
        self._active_model_version: str = getattr(config, 'active_embedding_model_version', '1.0.0')
        logger.info("Index lifecycle manager initialized.")

    # -------------------------------------------------------------------
    # Event-Driven Indexing
    # -------------------------------------------------------------------

    def on_data_change(self, source_name: str, change_type: str = "write") -> Optional[IndexJob]:
        """
        Handle a data change event from an MCP server.
        This is the core automation: the data flow IS the indexing trigger.
        """
        source = self.router.get_source(source_name)
        if not source:
            logger.warning(f"Data change event for unknown source: {source_name}")
            return None

        if source.index_strategy == "none":
            return None  # no index needed

        # Check circuit breaker
        breaker = self._get_breaker(source_name)
        if not breaker.can_retry():
            logger.warning(f"Circuit breaker open for {source_name} — skipping re-index")
            return None

        # Queue re-index
        job = self._create_job(
            source_name=source_name,
            job_type="incremental",
            strategy=source.index_strategy,
            trigger="data_change",
        )

        logger.info(f"Index job queued: {job.id} for {source_name} (trigger: data_change)")
        return job

    def on_model_change(self, new_model: str, new_version: str) -> list[IndexJob]:
        """
        Handle embedding model update.
        When the model changes, ALL vector indexes are silently invalid.
        Old embeddings and new embeddings aren't comparable.
        This catches that and triggers full rebuilds.
        """
        old_model = self._active_model
        old_version = self._active_model_version
        self._active_model = new_model
        self._active_model_version = new_version

        jobs = []
        for source in self.router.list_sources():
            if source.index_strategy in ("vector", "hybrid"):
                if source.embedding_model != new_model or source.embedding_model_version != new_version:
                    job = self._create_job(
                        source_name=source.name,
                        job_type="rebuild_model_change",
                        strategy=source.index_strategy,
                        trigger=f"model_change: {old_model}@{old_version} → {new_model}@{new_version}",
                    )
                    jobs.append(job)

        logger.info(f"Embedding model changed: {len(jobs)} indexes queued for rebuild")
        return jobs

    def on_schema_change(self, source_name: str, new_fingerprint: str) -> Optional[IndexJob]:
        """
        Handle data schema change.
        If the shape of the data changes, the index may be invalid.
        Quarantine and rebuild.
        """
        source = self.router.get_source(source_name)
        if not source:
            return None

        if source.schema_fingerprint and source.schema_fingerprint != new_fingerprint:
            # Schema changed — quarantine existing index
            health = self.router._index_health.get(source_name)
            if health:
                health.status = "corrupted"
                health.schema_match = False

            source.schema_fingerprint = new_fingerprint
            job = self._create_job(
                source_name=source_name,
                job_type="rebuild_schema_change",
                strategy=source.index_strategy,
                trigger=f"schema_change: {source.schema_fingerprint} → {new_fingerprint}",
            )
            logger.warning(f"Schema change detected for {source_name} — index quarantined, rebuild queued")
            return job

        source.schema_fingerprint = new_fingerprint
        return None

    # -------------------------------------------------------------------
    # Heartbeat Check
    # -------------------------------------------------------------------

    def heartbeat(self) -> dict:
        """
        Periodic health check across all sources.
        Catches stale indexes that weren't caught by event-driven triggers
        (e.g., if the data changed but no write event was emitted).
        """
        results = {"checked": 0, "stale": 0, "rebuilt": 0, "circuit_breaker_open": 0}

        for source in self.router.list_sources():
            results["checked"] += 1
            health = self.router._check_index_health(source)

            breaker = self._get_breaker(source.name)
            if breaker.is_tripped:
                results["circuit_breaker_open"] += 1
                continue

            if health.status == "stale":
                results["stale"] += 1
                self._create_job(
                    source_name=source.name,
                    job_type="incremental",
                    strategy=source.index_strategy,
                    trigger="heartbeat_stale",
                )
                results["rebuilt"] += 1

            elif health.status == "corrupted":
                self._create_job(
                    source_name=source.name,
                    job_type="full_build",
                    strategy=source.index_strategy,
                    trigger="heartbeat_corrupted",
                )
                results["rebuilt"] += 1

            elif health.status == "missing" and source.index_strategy != "none":
                self._create_job(
                    source_name=source.name,
                    job_type="full_build",
                    strategy=source.index_strategy,
                    trigger="heartbeat_missing",
                )
                results["rebuilt"] += 1

        logger.info(
            f"Heartbeat: {results['checked']} checked, "
            f"{results['stale']} stale, {results['rebuilt']} rebuilds queued, "
            f"{results['circuit_breaker_open']} circuit breakers open"
        )
        return results

    # -------------------------------------------------------------------
    # Job Execution
    # -------------------------------------------------------------------

    def process_queue(self) -> list[IndexJob]:
        """
        Process pending index jobs.
        In production, this runs as a background worker.
        BM25 rebuilds run inline (they're fast).
        Vector rebuilds run async (they take longer).
        """
        completed = []

        while self._job_queue:
            job = self._job_queue.pop(0)
            breaker = self._get_breaker(job.source_name)

            if not breaker.can_retry():
                job.status = "failed"
                job.error = "Circuit breaker open"
                self._job_history.append(job)
                continue

            start = time.time()
            try:
                job.status = "running"
                self._execute_index_job(job)
                job.status = "completed"
                job.completed_at = datetime.utcnow().isoformat()
                breaker.record_success()

                # Update source metadata
                source = self.router.get_source(job.source_name)
                if source:
                    source.last_indexed_at = job.completed_at
                    if job.strategy in ("vector", "hybrid"):
                        source.embedding_model = self._active_model
                        source.embedding_model_version = self._active_model_version

            except Exception as e:
                job.status = "failed"
                job.error = str(e)
                breaker.record_failure()
                logger.error(f"Index job {job.id} failed: {e}")

            job.duration_ms = int((time.time() - start) * 1000)
            self._job_history.append(job)
            completed.append(job)

        return completed

    def _execute_index_job(self, job: IndexJob):
        """
        Execute a single index job.
        Stub — production integrates with actual index backends.

        BM25: uses rank_bm25 or tantivy — sub-second for most corpora
        Vector: uses sentence-transformers locally — minutes for large corpora
        Hybrid: both
        """
        logger.info(f"Executing index job {job.id}: {job.job_type} on {job.source_name} ({job.strategy})")

        if job.strategy == "bm25":
            # BM25 rebuilds are fast — inline execution
            job.documents_processed = self._rebuild_bm25(job.source_name)
        elif job.strategy == "vector":
            # Vector rebuilds are slower — would be async in production
            job.documents_processed = self._rebuild_vector(job.source_name)
        elif job.strategy == "hybrid":
            job.documents_processed = self._rebuild_bm25(job.source_name)
            job.documents_processed += self._rebuild_vector(job.source_name)

    def _rebuild_bm25(self, source_name: str) -> int:
        """Rebuild BM25 index. Stub — production uses rank_bm25 or tantivy."""
        logger.debug(f"Rebuilding BM25 index for {source_name}")
        return 0  # stub: return document count

    def _rebuild_vector(self, source_name: str) -> int:
        """Rebuild vector index. Stub — production uses sentence-transformers locally."""
        logger.debug(f"Rebuilding vector index for {source_name} using {self._active_model}")
        return 0  # stub: return document count

    # -------------------------------------------------------------------
    # Circuit Breaker Management
    # -------------------------------------------------------------------

    def _get_breaker(self, source_name: str) -> CircuitBreakerState:
        if source_name not in self._circuit_breakers:
            self._circuit_breakers[source_name] = CircuitBreakerState(source_name=source_name)
        return self._circuit_breakers[source_name]

    def reset_circuit_breaker(self, source_name: str):
        """Manual reset — for when the underlying issue is fixed."""
        breaker = self._get_breaker(source_name)
        breaker.state = "closed"
        breaker.consecutive_failures = 0
        logger.info(f"Circuit breaker reset for {source_name}")

    # -------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------

    def _create_job(
        self,
        source_name: str,
        job_type: str,
        strategy: str,
        trigger: str,
    ) -> IndexJob:
        import uuid
        job = IndexJob(
            id=f"idx_{uuid.uuid4().hex[:8]}",
            source_name=source_name,
            job_type=job_type,
            strategy=strategy if strategy != "none" else "bm25",
            trigger=trigger,
        )
        self._job_queue.append(job)
        return job

    def compute_schema_fingerprint(self, data_sample: dict) -> str:
        """Compute a fingerprint of the data's schema (keys, types, nesting)."""
        def _schema_of(obj: Any, depth: int = 0) -> str:
            if depth > 5:
                return "..."
            if isinstance(obj, dict):
                parts = sorted(f"{k}:{_schema_of(v, depth+1)}" for k, v in obj.items())
                return "{" + ",".join(parts) + "}"
            elif isinstance(obj, list):
                if obj:
                    return f"[{_schema_of(obj[0], depth+1)}]"
                return "[]"
            else:
                return type(obj).__name__
        schema_str = _schema_of(data_sample)
        return hashlib.sha256(schema_str.encode()).hexdigest()[:16]

    # -------------------------------------------------------------------
    # Health
    # -------------------------------------------------------------------

    def health(self) -> dict:
        return {
            "status": "ok",
            "jobs_queued": len(self._job_queue),
            "jobs_completed": sum(1 for j in self._job_history if j.status == "completed"),
            "jobs_failed": sum(1 for j in self._job_history if j.status == "failed"),
            "circuit_breakers_open": sum(1 for b in self._circuit_breakers.values() if b.is_tripped),
            "active_model": f"{self._active_model}@{self._active_model_version}",
        }
