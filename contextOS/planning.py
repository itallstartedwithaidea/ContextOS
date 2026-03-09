"""
ContextOS Planning Layer

Extends:
  - gsd-build/get-shit-done (spec-driven execution)
  - dair-ai/Prompt-Engineering-Guide (prompt patterns)

New capabilities:
  - Pre-Response Sparring Hook (entirely new — does not exist in source repos)
  - Dynamic plan revision on tool failure
  - Constraint propagation
  - Spec versioning + diff
  - Outcome evaluation
"""

from __future__ import annotations
import uuid
import json
import logging
from datetime import datetime
from typing import Literal, Optional
from dataclasses import dataclass, field

logger = logging.getLogger("contextos.planning")


@dataclass
class SparringVerdict:
    """Result of a Pre-Response Sparring Hook evaluation."""
    verdict: Literal["PROCEED", "HOLD", "ESCALATE"]
    confidence: float
    reason: str
    missing_information: list[str] = field(default_factory=list)
    pattern_match_warning: Optional[str] = None
    recommended_action: str = ""
    latency_ms: int = 0
    tokens_used: int = 0


@dataclass
class Plan:
    """A spec-driven execution plan."""
    id: str = field(default_factory=lambda: f"plan_{uuid.uuid4().hex[:8]}")
    goal: str = ""
    spec: str = ""
    steps: list[dict] = field(default_factory=list)
    version: int = 1
    version_history: list[dict] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    outcome_score: Optional[float] = None
    status: Literal["draft", "active", "completed", "failed", "rolled_back"] = "draft"


class SparringHook:
    """
    The Pre-Response Sparring Hook.

    The single most important feature ContextOS adds that no source repo had.
    A mandatory reflection step before agent output that distinguishes
    solve-it moments from learn-more moments.

    Origin: Conceived by John Williams (IASAWI) from a practitioner insight
    about the pattern-matching blind spot in both human operators and AI agents.
    """

    SPARRING_SYSTEM_PROMPT = """You are a pre-response sparring partner for an AI agent.
Your job is NOT to answer the request. Your job is to evaluate whether the agent
has enough information and context to answer it correctly.

You must evaluate:
1. Is there sufficient information to act on this correctly?
2. Is the agent pattern-matching (recognizing a familiar shape) or actually
   reasoning about this specific situation?
3. What is the worst outcome if the agent acts now and is wrong?
   Is that outcome reversible?

Return a JSON object with exactly these fields:
{
  "verdict": "PROCEED" | "HOLD" | "ESCALATE",
  "confidence": 0.0-1.0,
  "reason": "one sentence explanation",
  "missing_information": ["list of specific things missing, or empty"],
  "pattern_match_warning": "describe the pattern being matched and how this situation might differ, or null",
  "recommended_action": "what the agent should do next"
}

PROCEED = enough context, safe to act
HOLD = need more information before acting
ESCALATE = action is high-stakes or irreversible, require human confirmation

Be direct. Be specific. Do not hedge."""

    def __init__(self, config):
        self.config = config
        self.threshold = config.sparring_threshold
        self.force_on_writes = config.sparring_on_writes
        self.force_on_irreversible = config.sparring_on_irreversible

    def should_fire(self, request: str, context: dict) -> bool:
        """Determine if sparring should run for this request."""
        if not self.config.sparring_hook:
            return False
        if self.threshold == "always":
            return True
        if self.threshold == "low":
            return context.get("is_irreversible", False)

        # Check for write/destructive operations
        write_signals = ["delete", "remove", "send", "publish", "update", "create", "modify"]
        is_write = any(signal in request.lower() for signal in write_signals)

        if self.force_on_writes and is_write:
            return True
        if self.force_on_irreversible and context.get("is_irreversible", False):
            return True
        if self.threshold == "high":
            return True  # Fire on everything when threshold is high
        # medium: fire on writes and low-confidence situations
        return is_write or context.get("confidence", 1.0) < 0.7

    def evaluate(
        self,
        request: str,
        context: str = "",
        prior_actions: list[str] = None,
    ) -> SparringVerdict:
        """
        Run the Pre-Response Sparring Hook evaluation.

        Args:
            request: The original agent request
            context: Available context summary
            prior_actions: List of actions already taken

        Returns:
            SparringVerdict with verdict and reasoning
        """
        import time
        start = time.time()

        prior_actions = prior_actions or []
        user_message = f"""REQUEST: {request}

CONTEXT AVAILABLE: {context or 'None'}

PRIOR ACTIONS TAKEN: {json.dumps(prior_actions) if prior_actions else 'None'}

Evaluate whether to PROCEED, HOLD, or ESCALATE."""

        # In production this calls the LLM. Stub for now.
        verdict = self._call_llm(user_message)

        elapsed_ms = int((time.time() - start) * 1000)
        verdict.latency_ms = elapsed_ms
        logger.info(
            f"Sparring Hook: verdict={verdict.verdict} "
            f"confidence={verdict.confidence:.2f} "
            f"latency={elapsed_ms}ms"
        )
        return verdict

    def _call_llm(self, message: str) -> SparringVerdict:
        """Call LLM for sparring evaluation. Override in production."""
        # Stub implementation — replace with actual LLM call
        return SparringVerdict(
            verdict="PROCEED",
            confidence=0.85,
            reason="Sufficient context available. No irreversible operations detected.",
            missing_information=[],
            pattern_match_warning=None,
            recommended_action="Proceed with execution.",
        )


class PlanningLayer:
    """
    ContextOS Planning Layer.

    Extends get-shit-done's spec-driven execution model with:
    - Pre-Response Sparring Hook (new)
    - Dynamic plan revision on tool failure (new)
    - Constraint propagation (new)
    - Spec versioning + diff (new)
    - Outcome evaluation (new)
    """

    def __init__(self, config):
        self.config = config
        self.sparring = SparringHook(config)
        self._plans: dict[str, Plan] = {}

    def spar(
        self,
        request: str,
        context: str = "",
        prior_actions: list[str] = None,
    ) -> SparringVerdict:
        """Run the Pre-Response Sparring Hook."""
        return self.sparring.evaluate(request, context, prior_actions or [])

    def create_plan(
        self,
        goal: str,
        context: str = "",
        constraints: list[str] = None,
        template: Optional[str] = None,
    ) -> Plan:
        """
        Generate a spec-driven execution plan.

        Adapted from get-shit-done's TÂCHES spec model with added:
        - Versioning from the start
        - Constraint tracking
        - Outcome evaluation hooks
        """
        plan = Plan(goal=goal)
        plan.spec = self._generate_spec(goal, context, constraints or [], template)
        plan.steps = self._decompose(goal, plan.spec, constraints or [])
        plan.status = "active"
        self._plans[plan.id] = plan
        logger.info(f"Plan created: {plan.id} with {len(plan.steps)} steps")
        return plan

    def revise_plan(
        self,
        plan_id: str,
        feedback: str,
        failed_step: Optional[str] = None,
        propagate_constraints: bool = True,
    ) -> Plan:
        """
        Dynamically revise a plan mid-execution.

        This is what get-shit-done was missing: plans that update
        when the world changes during execution, not just upfront.
        """
        plan = self._plans.get(plan_id)
        if not plan:
            raise ValueError(f"Plan not found: {plan_id}")

        # Snapshot current version to history
        plan.version_history.append({
            "version": plan.version,
            "steps": plan.steps.copy(),
            "spec": plan.spec,
            "revised_at": datetime.utcnow().isoformat(),
            "revision_reason": feedback,
        })

        plan.version += 1
        # In production: call LLM to revise steps based on feedback
        # For now: mark failed step and adjust downstream
        if failed_step and propagate_constraints:
            plan.steps = self._propagate_failure(plan.steps, failed_step, feedback)

        logger.info(f"Plan {plan_id} revised to v{plan.version} due to: {feedback}")
        return plan

    def evaluate_outcome(
        self,
        plan_id: str,
        output: str,
        criteria: list[str] = None,
    ) -> dict:
        """
        Score plan output against the original spec.
        Feeds signal back to improve future planning.
        """
        plan = self._plans.get(plan_id)
        if not plan:
            raise ValueError(f"Plan not found: {plan_id}")

        criteria = criteria or ["completeness", "accuracy", "spec_adherence"]
        # In production: LLM-based evaluation
        scores = {c: 0.85 for c in criteria}  # Stub
        plan.outcome_score = sum(scores.values()) / len(scores)
        plan.status = "completed"
        return {"plan_id": plan_id, "scores": scores, "overall": plan.outcome_score}

    def diff_plans(self, plan_id_a: str, plan_id_b: str) -> dict:
        """Diff two plan versions."""
        a = self._plans.get(plan_id_a)
        b = self._plans.get(plan_id_b)
        if not a or not b:
            raise ValueError("One or both plan IDs not found")
        return {
            "plan_a": plan_id_a,
            "plan_b": plan_id_b,
            "step_diff": self._diff_steps(a.steps, b.steps),
        }

    def rollback_plan(self, plan_id: str, target_version: Optional[str] = None) -> Plan:
        """Restore a previous plan version."""
        plan = self._plans.get(plan_id)
        if not plan:
            raise ValueError(f"Plan not found: {plan_id}")
        if not plan.version_history:
            raise ValueError(f"No history to roll back to for plan {plan_id}")

        target = plan.version_history[-1] if target_version == "previous" else \
                 next((h for h in plan.version_history if str(h["version"]) == target_version), None)

        if not target:
            raise ValueError(f"Target version not found: {target_version}")

        plan.steps = target["steps"]
        plan.spec = target["spec"]
        plan.version += 1
        plan.status = "active"
        logger.info(f"Plan {plan_id} rolled back to v{target['version']}")
        return plan

    def _generate_spec(self, goal: str, context: str, constraints: list, template: Optional[str]) -> str:
        """Generate a spec from a goal. Stub — LLM call in production."""
        return f"SPEC: {goal}\nCONSTRAINTS: {', '.join(constraints) or 'none'}"

    def _decompose(self, goal: str, spec: str, constraints: list) -> list[dict]:
        """Decompose a spec into executable steps. Stub — LLM call in production."""
        return [{"id": "step_1", "action": goal, "depends_on": [], "status": "pending"}]

    def _propagate_failure(self, steps: list, failed_step: str, reason: str) -> list:
        """Propagate a step failure to dependent steps."""
        failed_ids = {failed_step}
        for step in steps:
            if any(dep in failed_ids for dep in step.get("depends_on", [])):
                step["status"] = "blocked"
                step["blocked_reason"] = f"Dependency {failed_step} failed: {reason}"
                failed_ids.add(step["id"])
        return steps

    def _diff_steps(self, steps_a: list, steps_b: list) -> dict:
        """Produce a simple diff of two step lists."""
        ids_a = {s["id"] for s in steps_a}
        ids_b = {s["id"] for s in steps_b}
        return {
            "added": list(ids_b - ids_a),
            "removed": list(ids_a - ids_b),
            "common": list(ids_a & ids_b),
        }

    def health(self) -> dict:
        return {
            "status": "ok",
            "plans_active": sum(1 for p in self._plans.values() if p.status == "active"),
            "sparring_hook": self.config.sparring_hook,
            "sparring_threshold": self.config.sparring_threshold,
        }
