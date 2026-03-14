"""
ContextOS Cognition Layer

The layer that sits between retrieval and output.
Not retrieval. Not generation. Thinking.

Six cognitive primitives that no agent framework has built:
  1. Active Forgetting    — drop context that degrades output quality
  2. Reasoning Calibration — know how much thinking a problem deserves
  3. Synthesis Detection   — know when to think vs. when to retrieve
  4. Unknown Unknown Sensing — detect missing categories of information
  5. Productive Contradiction — hold conflicting data as signal, not noise
  6. Context-Dependent Gravity — re-weight memory/retrieval by current question

Origin: Identified by tracing how reasoning actually works in a live
conversation between John Williams (IASAWI) and an AI agent analyzing
the RAG retrieval debate (March 2026). The conversation itself became
the spec — each primitive was practiced before it was named.

This layer does not exist in any open-source agent framework as of March 2026.
"""

from __future__ import annotations
import logging
import time
from typing import Any, Literal, Optional
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger("contextos.cognition")


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class ContextBudget:
    """
    The RAM constraint nobody builds for.

    Karpathy: "LLM = CPU, Context Window = RAM."
    But every agent framework fills the window indiscriminately.
    This enforces a budget: how many tokens of retrieved context
    does this request actually deserve?
    """
    total_tokens: int = 8000
    allocated: int = 0
    by_source: dict[str, int] = field(default_factory=dict)
    overflow_policy: Literal["truncate_lowest", "drop_oldest", "reject"] = "truncate_lowest"

    @property
    def remaining(self) -> int:
        return max(0, self.total_tokens - self.allocated)

    def allocate(self, source: str, tokens: int) -> int:
        """Allocate tokens to a source. Returns actual tokens allocated."""
        actual = min(tokens, self.remaining)
        if actual > 0:
            self.by_source[source] = self.by_source.get(source, 0) + actual
            self.allocated += actual
        return actual

    def is_full(self) -> bool:
        return self.remaining == 0


@dataclass
class ForgettingDecision:
    """Result of active forgetting evaluation."""
    content_id: str
    action: Literal["keep", "discard", "compress"]
    reason: str
    noise_score: float  # 0.0 = pure signal, 1.0 = pure noise
    tokens_freed: int = 0


@dataclass
class ReasoningDepthEstimate:
    """How much thinking does this problem deserve?"""
    estimated_depth: Literal["pattern_match", "shallow", "moderate", "deep", "chain"]
    estimated_steps: int
    diminishing_returns_after: int  # step number where ROI drops
    reason: str
    confidence: float


@dataclass
class SynthesisOrRetrievalDecision:
    """Should the agent think about what it has, or go get more?"""
    decision: Literal["synthesize", "retrieve", "both"]
    reason: str
    gap_type: Optional[str] = None  # "factual", "relational", "causal", "analogical"
    retrieval_target: Optional[str] = None  # what to get if retrieve


@dataclass
class UnknownUnknownAlert:
    """
    Signal that the agent may be missing an entire category of information.
    Not 'I don't have the answer' — 'I don't know this question exists.'
    """
    alert_type: Literal["missing_source", "missing_dimension", "missing_stakeholder", "missing_constraint"]
    description: str
    confidence: float
    suggested_exploration: str  # what the agent should look for
    detected_by: str  # which heuristic caught it


@dataclass
class ContradictionReport:
    """
    Two data sources disagree. Instead of resolving, hold the tension.
    The contradiction itself may be the insight.
    """
    source_a: str
    source_b: str
    claim_a: str
    claim_b: str
    contradiction_type: Literal["factual", "temporal", "measurement", "framing"]
    resolution_attempted: bool = False
    insight_from_contradiction: Optional[str] = None  # what the disagreement tells us
    recommended_action: Literal["investigate", "report_both", "flag_measurement_gap", "defer"] = "investigate"


@dataclass
class GravityShift:
    """
    A memory or retrieved fact that changes importance based on the current question.
    Static importance scores miss this entirely.
    """
    memory_id: str
    original_importance: float
    contextual_importance: float  # re-scored for current question
    reason: str
    is_constraint: bool = False  # constraints are often low-similarity but high-impact


@dataclass
class CognitionReport:
    """
    Full cognition pass results.
    Attached to the Sparring Hook so it knows the quality of the thinking,
    not just the quality of the retrieval.
    """
    budget: ContextBudget
    forgotten: list[ForgettingDecision] = field(default_factory=list)
    depth_estimate: Optional[ReasoningDepthEstimate] = None
    synthesis_decision: Optional[SynthesisOrRetrievalDecision] = None
    unknown_unknowns: list[UnknownUnknownAlert] = field(default_factory=list)
    contradictions: list[ContradictionReport] = field(default_factory=list)
    gravity_shifts: list[GravityShift] = field(default_factory=list)
    latency_ms: int = 0
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


# ---------------------------------------------------------------------------
# Cognition Layer
# ---------------------------------------------------------------------------

class CognitionLayer:
    """
    The thinking layer between retrieval and output.

    Every agent framework in the industry builds:
        retrieve → generate

    ContextOS builds:
        retrieve → THINK → generate

    This layer implements six cognitive primitives that model how
    expert reasoning actually works, derived from tracing the process
    in live conversation.
    """

    def __init__(self, config):
        self.config = config
        self._forgetting_log: list[ForgettingDecision] = []
        self._contradiction_history: list[ContradictionReport] = []
        self._depth_calibration_data: list[dict] = []  # learns over time
        logger.info("Cognition layer initialized. Six primitives active.")

    # -------------------------------------------------------------------
    # Primitive 1: Active Forgetting
    # -------------------------------------------------------------------

    def forget(
        self,
        retrieved_context: list[dict],
        query: str,
        budget: ContextBudget,
    ) -> tuple[list[dict], list[ForgettingDecision]]:
        """
        Active forgetting: drop context that degrades output quality.

        The industry is obsessed with putting MORE into the context window.
        This does the opposite — removes what hurts.

        Filters:
        1. Noise score: how much of this chunk is relevant to the query?
        2. Redundancy: does this chunk repeat what another already covers?
        3. Budget: does including this chunk displace something more valuable?

        Returns:
            (kept_context, forgetting_decisions)
        """
        kept = []
        decisions = []

        # Score each chunk for noise
        scored = []
        for item in retrieved_context:
            noise = self._estimate_noise(item, query)
            scored.append((item, noise))

        # Sort by signal strength (lowest noise first)
        scored.sort(key=lambda x: x[1])

        # Deduplicate — check semantic redundancy
        seen_signals = []
        for item, noise in scored:
            if noise > 0.7:
                decisions.append(ForgettingDecision(
                    content_id=item.get("id", "unknown"),
                    action="discard",
                    reason="Noise score too high — content is not relevant to the current query",
                    noise_score=noise,
                    tokens_freed=item.get("token_count", 0),
                ))
                continue

            if self._is_redundant(item, seen_signals):
                decisions.append(ForgettingDecision(
                    content_id=item.get("id", "unknown"),
                    action="discard",
                    reason="Redundant with already-kept context",
                    noise_score=noise,
                    tokens_freed=item.get("token_count", 0),
                ))
                continue

            token_count = item.get("token_count", 200)
            allocated = budget.allocate(item.get("source", "unknown"), token_count)
            if allocated == 0:
                decisions.append(ForgettingDecision(
                    content_id=item.get("id", "unknown"),
                    action="discard",
                    reason="Context budget exhausted",
                    noise_score=noise,
                    tokens_freed=token_count,
                ))
                continue

            kept.append(item)
            seen_signals.append(item)
            decisions.append(ForgettingDecision(
                content_id=item.get("id", "unknown"),
                action="keep",
                reason="Below noise threshold, not redundant, within budget",
                noise_score=noise,
            ))

        self._forgetting_log.extend(decisions)
        logger.info(
            f"Active forgetting: {len(retrieved_context)} in → "
            f"{len(kept)} kept, {len(retrieved_context) - len(kept)} dropped"
        )
        return kept, decisions

    # -------------------------------------------------------------------
    # Primitive 2: Reasoning Depth Calibration
    # -------------------------------------------------------------------

    def calibrate_depth(
        self,
        query: str,
        available_context: list[dict],
        prior_turns: int = 0,
    ) -> ReasoningDepthEstimate:
        """
        How much thinking does this problem deserve?

        A fast pattern match and a 10-step chain of reasoning
        are both valid — for different problems. The agent should
        know which situation it's in BEFORE committing the compute.

        Signals:
        - Query complexity (single fact vs. multi-factor analysis)
        - Context ambiguity (clear answer available vs. conflicting signals)
        - Stakes (reversible action vs. irreversible commitment)
        - Novelty (seen this pattern before vs. new territory)
        """
        complexity = self._estimate_complexity(query)
        ambiguity = self._estimate_ambiguity(available_context)
        stakes = self._estimate_stakes(query)

        # Map to depth level
        score = (complexity * 0.4) + (ambiguity * 0.3) + (stakes * 0.3)

        if score < 0.2:
            depth = "pattern_match"
            steps = 1
            diminishing = 1
        elif score < 0.4:
            depth = "shallow"
            steps = 2
            diminishing = 2
        elif score < 0.6:
            depth = "moderate"
            steps = 4
            diminishing = 3
        elif score < 0.8:
            depth = "deep"
            steps = 7
            diminishing = 5
        else:
            depth = "chain"
            steps = 10
            diminishing = 7

        estimate = ReasoningDepthEstimate(
            estimated_depth=depth,
            estimated_steps=steps,
            diminishing_returns_after=diminishing,
            reason=f"Complexity={complexity:.2f}, Ambiguity={ambiguity:.2f}, Stakes={stakes:.2f}",
            confidence=0.75,
        )

        # Store for calibration learning
        self._depth_calibration_data.append({
            "query": query,
            "estimate": depth,
            "score": score,
            "timestamp": datetime.utcnow().isoformat(),
        })

        logger.info(f"Depth calibration: {depth} ({steps} steps, diminishing after {diminishing})")
        return estimate

    # -------------------------------------------------------------------
    # Primitive 3: Synthesis vs. Retrieval Detection
    # -------------------------------------------------------------------

    def should_think_or_retrieve(
        self,
        query: str,
        available_context: list[dict],
        memory_entries: list = None,
    ) -> SynthesisOrRetrievalDecision:
        """
        Does the agent need to GET more information, or THINK about
        what it already has?

        The entire industry treats every task as a retrieval problem.
        But some tasks are:
        - Synthesis: "What pattern connects these three things?"
        - Analogy: "How is this like that other domain?"
        - Relational: "Hold five things in working memory and find connections"

        These aren't retrieval tasks. They're reasoning tasks.
        Retrieving more data actively hurts them by diluting focus.
        """
        gap = self._identify_gap_type(query, available_context, memory_entries or [])

        if gap["type"] == "none":
            return SynthesisOrRetrievalDecision(
                decision="synthesize",
                reason="Sufficient information available. Reasoning required, not retrieval.",
                gap_type=None,
            )
        elif gap["type"] in ("factual", "temporal"):
            return SynthesisOrRetrievalDecision(
                decision="retrieve",
                reason=f"Missing {gap['type']} information: {gap['description']}",
                gap_type=gap["type"],
                retrieval_target=gap.get("target"),
            )
        elif gap["type"] in ("causal", "analogical"):
            return SynthesisOrRetrievalDecision(
                decision="synthesize",
                reason=f"Gap is {gap['type']} — more data won't help, deeper reasoning will.",
                gap_type=gap["type"],
            )
        else:
            return SynthesisOrRetrievalDecision(
                decision="both",
                reason=f"Mixed gap: need data for {gap.get('retrieve_part', '?')} and reasoning for {gap.get('think_part', '?')}",
                gap_type=gap["type"],
                retrieval_target=gap.get("target"),
            )

    # -------------------------------------------------------------------
    # Primitive 4: Unknown Unknown Detection
    # -------------------------------------------------------------------

    def sense_unknown_unknowns(
        self,
        query: str,
        available_sources: list[str],
        retrieved_from: list[str],
        domain: str = "general",
    ) -> list[UnknownUnknownAlert]:
        """
        Detect when the agent might be missing an entire CATEGORY
        of information, not just a specific fact.

        Known unknowns: "I don't have today's auction data."
        Unknown unknowns: "I didn't know Salesforce data was relevant here."

        Heuristics:
        1. Source coverage: are there known source types for this domain
           that weren't queried?
        2. Dimensional analysis: does the query imply multiple dimensions
           (cost, revenue, time, audience) and are any unrepresented?
        3. Stakeholder check: does the decision affect parties whose
           data wasn't consulted?
        4. Constraint scan: are there known constraints (policies, budgets,
           legal) that weren't retrieved?
        """
        alerts = []

        # Source coverage heuristic
        expected_sources = self._expected_sources_for_domain(domain)
        missing_sources = [s for s in expected_sources if s not in retrieved_from]
        for source in missing_sources:
            if source in available_sources:
                alerts.append(UnknownUnknownAlert(
                    alert_type="missing_source",
                    description=f"Source '{source}' is available but was not queried. "
                                f"It may contain relevant information for this domain.",
                    confidence=0.6,
                    suggested_exploration=f"Query {source} for: {query}",
                    detected_by="source_coverage",
                ))

        # Dimensional analysis heuristic
        dimensions_in_query = self._detect_dimensions(query)
        dimensions_in_context = self._detect_dimensions(
            " ".join(retrieved_from)  # simplified — full context in production
        )
        missing_dimensions = dimensions_in_query - dimensions_in_context
        for dim in missing_dimensions:
            alerts.append(UnknownUnknownAlert(
                alert_type="missing_dimension",
                description=f"Query implies '{dim}' dimension but retrieved context "
                            f"doesn't cover it.",
                confidence=0.5,
                suggested_exploration=f"Find data covering the '{dim}' dimension",
                detected_by="dimensional_analysis",
            ))

        logger.info(f"Unknown-unknown scan: {len(alerts)} alerts")
        return alerts

    # -------------------------------------------------------------------
    # Primitive 5: Productive Contradiction
    # -------------------------------------------------------------------

    def detect_contradictions(
        self,
        retrieved_context: list[dict],
        resolve: bool = False,
    ) -> list[ContradictionReport]:
        """
        Find where data sources disagree.
        Instead of always resolving — hold the contradiction as signal.

        "Google Ads says conversions are up. CRM says pipeline is flat."
        The answer isn't "pick one." The answer is "there's a measurement
        gap and THAT is the insight."

        Types:
        - Factual: two sources state different facts
        - Temporal: data from different time periods conflict
        - Measurement: different metrics tell different stories
        - Framing: same data, different interpretations
        """
        contradictions = []

        # Pairwise comparison of claims across sources
        for i, item_a in enumerate(retrieved_context):
            for item_b in retrieved_context[i + 1:]:
                if item_a.get("source") == item_b.get("source"):
                    continue  # same source, skip

                conflict = self._detect_conflict(item_a, item_b)
                if conflict:
                    report = ContradictionReport(
                        source_a=item_a.get("source", "unknown"),
                        source_b=item_b.get("source", "unknown"),
                        claim_a=item_a.get("content", "")[:200],
                        claim_b=item_b.get("content", "")[:200],
                        contradiction_type=conflict["type"],
                    )

                    if not resolve:
                        # The productive path: extract insight from the contradiction
                        report.insight_from_contradiction = conflict.get("insight")
                        report.recommended_action = "report_both"
                    else:
                        report.resolution_attempted = True
                        report.recommended_action = "investigate"

                    contradictions.append(report)

        self._contradiction_history.extend(contradictions)
        logger.info(f"Contradiction detection: {len(contradictions)} found")
        return contradictions

    # -------------------------------------------------------------------
    # Primitive 6: Context-Dependent Gravity
    # -------------------------------------------------------------------

    def reweight_by_gravity(
        self,
        memories: list[dict],
        current_query: str,
        current_context: dict = None,
    ) -> list[GravityShift]:
        """
        Re-score memory importance based on the current question.

        Static importance scores are wrong. A memory about "client said
        never run on branded terms" scores low on similarity to a PMax
        optimization query — but it fundamentally changes the answer.

        This finds the memories that DON'T pattern-match but DO matter:
        - Constraints that apply to the current domain
        - Historical decisions that set precedent
        - Cross-domain insights that transfer
        """
        shifts = []

        for memory in memories:
            original = memory.get("importance", 0.5)
            content = memory.get("content", "")

            # Check if this is a constraint that applies
            is_constraint = self._is_applicable_constraint(content, current_query)

            # Check if this is a precedent
            is_precedent = self._is_relevant_precedent(content, current_query)

            # Check for cross-domain transfer
            is_transfer = self._is_cross_domain_relevant(content, current_query)

            # Calculate contextual importance
            contextual = original
            reason_parts = []

            if is_constraint:
                contextual = max(contextual, 0.95)  # constraints override similarity
                reason_parts.append("Applicable constraint detected")
            if is_precedent:
                contextual = max(contextual, 0.8)
                reason_parts.append("Relevant historical precedent")
            if is_transfer:
                contextual = max(contextual, 0.7)
                reason_parts.append("Cross-domain insight applies")

            if abs(contextual - original) > 0.1:
                shifts.append(GravityShift(
                    memory_id=memory.get("id", "unknown"),
                    original_importance=original,
                    contextual_importance=contextual,
                    reason="; ".join(reason_parts) if reason_parts else "No shift",
                    is_constraint=is_constraint,
                ))

        logger.info(f"Gravity reweighting: {len(shifts)} memories shifted")
        return shifts

    # -------------------------------------------------------------------
    # Full Cognition Pass
    # -------------------------------------------------------------------

    def think(
        self,
        query: str,
        retrieved_context: list[dict],
        memories: list[dict] = None,
        available_sources: list[str] = None,
        retrieved_from: list[str] = None,
        domain: str = "general",
        budget_tokens: int = 8000,
    ) -> CognitionReport:
        """
        Run the full cognition pass.

        This is the method that fires between retrieval and generation.
        Every primitive runs. The CognitionReport feeds into the
        Sparring Hook so it knows the quality of the THINKING,
        not just the quality of the retrieval.
        """
        start = time.time()
        budget = ContextBudget(total_tokens=budget_tokens)

        # 1. Active Forgetting
        kept_context, forgotten = self.forget(retrieved_context, query, budget)

        # 2. Reasoning Depth Calibration
        depth = self.calibrate_depth(query, kept_context)

        # 3. Synthesis vs. Retrieval
        synthesis = self.should_think_or_retrieve(query, kept_context, memories)

        # 4. Unknown Unknown Detection
        unknowns = self.sense_unknown_unknowns(
            query,
            available_sources or [],
            retrieved_from or [],
            domain,
        )

        # 5. Productive Contradiction
        contradictions = self.detect_contradictions(kept_context, resolve=False)

        # 6. Context-Dependent Gravity
        gravity = self.reweight_by_gravity(memories or [], query)

        elapsed = int((time.time() - start) * 1000)

        report = CognitionReport(
            budget=budget,
            forgotten=forgotten,
            depth_estimate=depth,
            synthesis_decision=synthesis,
            unknown_unknowns=unknowns,
            contradictions=contradictions,
            gravity_shifts=gravity,
            latency_ms=elapsed,
        )

        logger.info(
            f"Cognition pass complete: {elapsed}ms | "
            f"Kept {len(kept_context)}/{len(retrieved_context)} context | "
            f"Depth: {depth.estimated_depth} | "
            f"Decision: {synthesis.decision} | "
            f"{len(unknowns)} unknown-unknowns | "
            f"{len(contradictions)} contradictions | "
            f"{len(gravity)} gravity shifts"
        )

        return report

    # -------------------------------------------------------------------
    # Self-Learning: calibrate from outcomes
    # -------------------------------------------------------------------

    def learn_from_outcome(
        self,
        cognition_report: CognitionReport,
        outcome_score: float,
        request_id: str,
    ):
        """
        Close the loop: after the agent produces output and it's evaluated,
        feed the result back to calibrate the cognition primitives.

        Did active forgetting help or hurt? Was the depth estimate right?
        Did the unknown-unknown alerts catch real gaps?
        """
        # Store calibration signal
        calibration = {
            "request_id": request_id,
            "depth_estimated": cognition_report.depth_estimate.estimated_depth if cognition_report.depth_estimate else None,
            "outcome_score": outcome_score,
            "unknowns_flagged": len(cognition_report.unknown_unknowns),
            "contradictions_found": len(cognition_report.contradictions),
            "context_kept_ratio": (
                cognition_report.budget.allocated / cognition_report.budget.total_tokens
                if cognition_report.budget.total_tokens > 0 else 0
            ),
            "timestamp": datetime.utcnow().isoformat(),
        }
        self._depth_calibration_data.append(calibration)
        logger.info(f"Cognition calibration recorded: outcome={outcome_score:.2f}")

    # -------------------------------------------------------------------
    # Internal heuristics (stubs — LLM or classifier in production)
    # -------------------------------------------------------------------

    def _estimate_noise(self, item: dict, query: str) -> float:
        """Estimate how much of this chunk is noise relative to the query."""
        # Stub: production uses embedding similarity + keyword overlap
        return 0.3

    def _is_redundant(self, item: dict, existing: list[dict]) -> bool:
        """Check if item is semantically redundant with already-kept context."""
        # Stub: production uses pairwise similarity check
        return False

    def _estimate_complexity(self, query: str) -> float:
        """Score query complexity 0-1."""
        # Simple heuristic: word count and question words as proxy
        words = query.split()
        multi_part = any(w in query.lower() for w in ["and", "compare", "analyze", "vs", "between", "relationship"])
        return min(1.0, (len(words) / 30) + (0.3 if multi_part else 0.0))

    def _estimate_ambiguity(self, context: list[dict]) -> float:
        """Score how ambiguous the available context is."""
        if not context:
            return 0.8  # no context = high ambiguity
        # Stub: production checks for conflicting signals, missing fields
        return 0.4

    def _estimate_stakes(self, query: str) -> float:
        """Score how high-stakes the action is."""
        high_stakes = ["delete", "send", "publish", "bid", "budget", "spend", "commit", "launch"]
        return 0.8 if any(w in query.lower() for w in high_stakes) else 0.3

    def _identify_gap_type(self, query: str, context: list, memories: list) -> dict:
        """Identify what TYPE of information gap exists."""
        # Stub: production uses LLM classification
        if not context and not memories:
            return {"type": "factual", "description": "No context available", "target": "all"}
        return {"type": "none", "description": "Context appears sufficient"}

    def _expected_sources_for_domain(self, domain: str) -> list[str]:
        """Return expected data sources for a given domain."""
        domain_sources = {
            "advertising": ["google_ads", "analytics", "crm", "budget", "creative_assets"],
            "sales": ["crm", "email", "calendar", "pipeline", "contracts"],
            "engineering": ["codebase", "docs", "tickets", "monitoring", "deploys"],
            "general": [],
        }
        return domain_sources.get(domain, [])

    def _detect_dimensions(self, text: str) -> set[str]:
        """Detect analytical dimensions referenced in text."""
        dimension_keywords = {
            "cost": {"cost", "spend", "budget", "price", "cpc", "cpa"},
            "revenue": {"revenue", "roas", "roi", "conversion", "sales"},
            "time": {"trend", "month", "quarter", "year", "week", "daily"},
            "audience": {"audience", "segment", "demographic", "cohort", "user"},
            "competitive": {"competitor", "market share", "benchmark", "industry"},
        }
        found = set()
        text_lower = text.lower()
        for dim, keywords in dimension_keywords.items():
            if any(kw in text_lower for kw in keywords):
                found.add(dim)
        return found

    def _detect_conflict(self, item_a: dict, item_b: dict) -> Optional[dict]:
        """Detect if two items contain contradictory claims."""
        # Stub: production uses LLM or NLI model for contradiction detection
        return None

    def _is_applicable_constraint(self, content: str, query: str) -> bool:
        """Check if a memory contains a constraint relevant to the query."""
        constraint_signals = ["never", "don't", "must not", "always", "required", "policy", "limit", "cap"]
        return any(s in content.lower() for s in constraint_signals)

    def _is_relevant_precedent(self, content: str, query: str) -> bool:
        """Check if a memory is a historical precedent for the current question."""
        precedent_signals = ["decided", "chose", "approved", "rejected", "learned", "last time"]
        return any(s in content.lower() for s in precedent_signals)

    def _is_cross_domain_relevant(self, content: str, query: str) -> bool:
        """Check if a memory from a different domain transfers to this query."""
        # Stub: production uses embedding similarity with domain-crossing bonus
        return False

    # -------------------------------------------------------------------
    # Health
    # -------------------------------------------------------------------

    def health(self) -> dict:
        return {
            "status": "ok",
            "forgetting_decisions_logged": len(self._forgetting_log),
            "contradictions_detected": len(self._contradiction_history),
            "calibration_data_points": len(self._depth_calibration_data),
            "primitives_active": 6,
        }
