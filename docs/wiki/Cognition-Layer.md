# Cognition Layer

> **The layer that sits between retrieval and output. Not retrieval. Not generation. Thinking.**

The Cognition Layer is entirely new in v0.2.0. No open-source agent framework has built it. It implements six cognitive primitives that model how expert reasoning actually works, derived from tracing the reasoning process in live problem-solving conversations.

---

## Why This Exists

Every agent framework in the market follows the same pipeline:

```
retrieve context → stuff into prompt → generate output
```

This skips the most important step. When a human expert gets information back from a search, they don't immediately write their answer. They:

- Discard the irrelevant results (active forgetting)
- Decide how deep to think about this (depth calibration)
- Ask whether they need more data or need to reason about what they have (synthesis detection)
- Wonder if they're missing an entire category of information (unknown-unknown sensing)
- Notice when two sources disagree and ask what the disagreement means (productive contradiction)
- Remember a constraint from months ago that changes the whole recommendation (context-dependent gravity)

These are cognitive primitives. They're the thinking that happens in the gap between retrieval and output. ContextOS makes them operational.

---

## The Six Primitives

### 1. Active Forgetting

**Problem:** The industry assumes more context = better output. It doesn't. Retrieving 20 chunks when 3 are useful creates noise that degrades reasoning quality.

**How it works:** The forgetting engine scores every retrieved chunk for noise (relevance to the current query), checks for redundancy against already-kept context, and enforces a context budget. Chunks that score above the noise threshold or exceed the budget are actively discarded before reasoning begins.

**Key concept -- Context Budget:** Karpathy said "LLM = CPU, Context Window = RAM." But nobody builds for the RAM constraint. The Context Budget enforces a hard token limit on retrieved context per request. It forces the system to keep only what earns its space.

```python
from contextos.cognition import ContextBudget

budget = ContextBudget(total_tokens=4000)

# After forgetting pass:
# 20 retrieved chunks → 5 kept
# 15 discarded: 8 noise, 4 redundant, 3 over budget
```

---

### 2. Reasoning Depth Calibration

**Problem:** Agents either think for a fixed number of steps or until an arbitrary quality threshold. Neither is right. A fast pattern match and a 10-step chain of reasoning are both valid -- for different problems.

**How it works:** Before the agent commits compute, the calibrator estimates problem complexity (single fact vs. multi-factor analysis), context ambiguity (clear answer vs. conflicting signals), and stakes (reversible action vs. irreversible commitment). These produce a depth recommendation: pattern_match, shallow, moderate, deep, or chain.

**Key concept -- Diminishing Returns:** Each depth level includes a "diminishing returns after step N" marker. This tells the agent when additional reasoning is unlikely to change the answer. Stop there.

```python
estimate = ctx.cognition().calibrate_depth(
    query="should I pause branded campaigns given declining ROAS",
    available_context=[...],
)

# estimate.estimated_depth = "moderate"
# estimate.estimated_steps = 4
# estimate.diminishing_returns_after = 3
# Reason: Complexity=0.47, Ambiguity=0.40, Stakes=0.80
```

---

### 3. Synthesis Detection

**Problem:** The industry treats every agent task as a retrieval problem. But some tasks are synthesis problems, analogy problems, or "hold five things in working memory and find the relationship" problems. Retrieving more data actively hurts these.

**How it works:** The synthesis detector classifies the information gap. Factual gaps ("I don't have today's data") need retrieval. Causal gaps ("why did this happen") and analogical gaps ("how is this like that") need reasoning. The detector tells the agent whether to retrieve or think.

**Gap types:**
- `factual` -- missing a specific data point → retrieve
- `temporal` -- data is outdated → retrieve
- `causal` -- need to understand why → synthesize
- `analogical` -- need to connect domains → synthesize
- mixed -- need both

```python
decision = ctx.cognition().should_think_or_retrieve(
    query="what pattern connects our Q1 campaigns to pipeline growth",
    available_context=[...],
    memory_entries=[...],
)

# decision.decision = "synthesize"
# decision.gap_type = "causal"
# decision.reason = "Gap is causal — more data won't help, deeper reasoning will."
```

---

### 4. Unknown Unknown Sensing

**Problem:** Agents search known corpora well. They have no idea when they're missing an entire category of information. "I didn't know Salesforce data was relevant here" is a fundamentally different failure mode than "I don't have today's report."

**How it works:** Four heuristics run on every cognition pass:
1. **Source coverage:** For the current domain, which expected data sources weren't queried?
2. **Dimensional analysis:** Does the query imply dimensions (cost, revenue, time, audience) that are unrepresented in retrieved context?
3. **Stakeholder check:** Does the decision affect parties whose data wasn't consulted?
4. **Constraint scan:** Are there known constraints (policies, budgets) that weren't retrieved?

**Advertising domain example:**

```python
report = ctx.cognition().think(
    query="should I pause branded campaigns",
    available_sources=["google_ads", "crm", "analytics", "budget", "creative"],
    retrieved_from=["google_ads", "analytics"],
    domain="advertising",
    ...
)

# report.unknown_unknowns:
# - missing_source: "crm" available but not queried
# - missing_source: "budget" available but not queried
# - missing_dimension: query implies "revenue" but context doesn't cover it
```

The system doesn't just tell you the answer is incomplete. It tells you WHERE to look.

---

### 5. Productive Contradiction

**Problem:** When two data sources disagree, every system resolves the conflict: pick the newer one, the more authoritative one, or average them. But sometimes the contradiction IS the insight.

**How it works:** Pairwise comparison of claims across sources. When a contradiction is detected, it's classified by type (factual, temporal, measurement, framing) and -- crucially -- the system extracts what the contradiction MEANS instead of resolving it.

**Contradiction types:**
- `factual` -- two sources state different facts
- `temporal` -- data from different time periods conflict
- `measurement` -- different metrics tell different stories
- `framing` -- same data, different interpretations

```python
contradictions = ctx.cognition().detect_contradictions(
    retrieved_context=[
        {"source": "google_ads", "content": "branded ROAS down 15% MoM"},
        {"source": "crm", "content": "pipeline up 20% MoM"},
    ],
    resolve=False,  # hold the tension
)

# The ROAS decline and pipeline growth aren't contradictory —
# they reveal a measurement gap between ad platform attribution
# and actual business impact. That IS the insight.
```

---

### 6. Context-Dependent Gravity

**Problem:** Memory systems retrieve by similarity to the query. But the memory that matters most is often the one that's LEAST similar -- a constraint that doesn't pattern-match but fundamentally changes the answer.

**How it works:** After retrieval, the gravity engine re-scores every memory and retrieved fact against three checks:

1. **Constraint detection:** Does this contain a policy, rule, or hard limit that applies to the current domain? If yes, boost to 0.95 regardless of similarity score.
2. **Precedent detection:** Is this a historical decision that sets precedent for the current question? If yes, boost to 0.8.
3. **Cross-domain transfer:** Does this insight from another domain apply here? If yes, boost to 0.7.

**The classic example:**

A memory says "client said never pause branded without approval." It sits at importance 0.3. The current query is about Performance Max optimization -- no keyword overlap with "branded." A similarity search would never surface it.

But the gravity engine detects "never" + "without approval" as a constraint signal, checks that it applies to the advertising domain, and boosts it to 0.95. Now it's the most important piece of context in the window.

```python
shifts = ctx.cognition().reweight_by_gravity(
    memories=[
        {"id": "m1", "content": "never pause branded without approval", "importance": 0.3},
        {"id": "m2", "content": "Q1 brand awareness priority", "importance": 0.4},
    ],
    current_query="should I pause branded campaigns given declining ROAS",
)

# m1: 0.3 → 0.95 (Applicable constraint detected)
# m2: 0.4 → 0.8  (Relevant historical precedent)
```

---

## Full Cognition Pass

All six primitives run together via `cognition.think()`:

```python
report = ctx.cognition().think(
    query="should I pause branded campaigns given declining ROAS",
    retrieved_context=[...],
    memories=[...],
    available_sources=["google_ads", "crm", "analytics", "budget"],
    retrieved_from=["google_ads", "analytics"],
    domain="advertising",
    budget_tokens=4000,
)

# report.budget           — token allocation across sources
# report.forgotten        — what was dropped and why
# report.depth_estimate   — how much thinking this deserves
# report.synthesis_decision — think or retrieve?
# report.unknown_unknowns — missing categories of info
# report.contradictions   — conflicting signals (held, not resolved)
# report.gravity_shifts   — memories that changed importance
```

The CognitionReport feeds into the Sparring Hook, giving it visibility into the quality of the THINKING, not just the quality of the retrieval.

---

## Self-Learning

After the agent produces output and it's evaluated:

```python
ctx.cognition().learn_from_outcome(
    cognition_report=report,
    outcome_score=0.87,
    request_id="req_abc123",
)
```

This closes the loop. The depth calibrator learns whether its estimates were right. The forgetting engine learns whether it dropped too much or too little. The system gets better at thinking over time.

---

## MCP Tools

| Tool | Description |
|---|---|
| `cognition_think` | Run full cognition pass |
| `cognition_forget` | Run active forgetting on context |
| `cognition_depth` | Get reasoning depth estimate |
| `cognition_contradictions` | Detect contradictions in context |
| `cognition_unknowns` | Run unknown-unknown sensing |
| `cognition_gravity` | Re-weight memories by current query |
