# The Pre-Response Sparring Hook

> *"The most expensive mistake an AI agent makes is the one it fires off before it has enough information."*

The Pre-Response Sparring Hook is ContextOS's most distinctive feature. It does not exist in any of the six source repositories. It is a mandatory reflection step that runs before any agent output and forces a single question: **Is this a solve-it moment or a learn-more moment?**

---

## The Problem It Solves

Every experienced operator knows this failure mode. You have a complex situation. Your first instinct is a point of view. You fire it off. Halfway through executing it you realize you were pattern-matching on a surface similarity, not actually understanding the specific context you were operating in.

This is the **pattern-matching blind spot** — the tendency to recognize a familiar shape in a problem and immediately act as if it's the same problem you've solved before, before fully gathering the information that would tell you whether it actually is.

AI agents have this problem at scale. They are trained on pattern recognition. Given an input, they generate the most statistically likely response. There is no native pause mechanism that says: "Before I generate this response, have I actually gathered enough context to generate the right one?"

The Pre-Response Sparring Hook is that pause mechanism.

---

## How It Works

When enabled (default: true), before any agent output is generated, the sparring hook intercepts and runs:

```
SPARRING EVALUATION
───────────────────
Input: {original_request}
Prior context available: {memory_summary}
Retrieved information: {retrieval_summary}
Tools executed: {tool_results}

QUESTION 1: Do I have enough information to act on this correctly?
  → If YES: proceed to execution
  → If NO: classify what's missing and request it

QUESTION 2: Am I pattern-matching, or am I actually reasoning about this specific situation?
  → Identify the closest prior pattern
  → List 2-3 ways this situation might differ from that pattern
  → If differences are material: flag for human review or more retrieval

QUESTION 3: What is the worst outcome if I act now and I'm wrong?
  → If reversible: proceed
  → If irreversible: require explicit confirmation or additional context
```

---

## Configuration

```python
from contextos import ContextOS

ctx = ContextOS(
    sparring_hook=True,           # Enable (default: True)
    sparring_threshold="medium",  # low | medium | high | always
    sparring_on_writes=True,      # Always spar before write operations
    sparring_on_irreversible=True # Always spar before irreversible actions
)
```

```json
// MCP config
{
  "sparring_hook": {
    "enabled": true,
    "threshold": "medium",
    "force_on_tool_types": ["write", "delete", "send", "execute"]
  }
}
```

### Threshold Levels

| Level | When Sparring Fires |
|---|---|
| `low` | Only on irreversible operations |
| `medium` | On writes, deletes, sends, and when confidence is below 0.7 |
| `high` | On any non-trivial operation |
| `always` | Before every single agent output |

---

## The `plan_spar` Tool

You can invoke the sparring hook directly as an MCP tool:

```json
{
  "tool": "plan_spar",
  "input": {
    "request": "Delete all campaigns with ROAS below 2.0",
    "context": "Q4 budget planning session",
    "prior_actions": ["retrieved campaign list", "calculated ROAS for all campaigns"]
  }
}
```

**Response:**
```json
{
  "verdict": "HOLD",
  "reason": "Operation is irreversible. 23 campaigns would be deleted. No confirmation that these campaigns are intended targets vs. brand campaigns where ROAS calculation methodology differs.",
  "missing_information": [
    "Are brand campaigns excluded from this threshold?",
    "Is this Q4 optimization or a permanent account restructure?",
    "Who is the approving stakeholder?"
  ],
  "pattern_match_warning": "This matches 'low-ROAS cleanup' pattern but Q4 pre-holiday context may make these campaigns strategic rather than inefficient.",
  "recommended_action": "Request confirmation with campaign list preview before executing."
}
```

---

## Why This Belongs in Infrastructure, Not Prompts

The natural question is: why can't you just add "pause and reflect before responding" to your system prompt?

The answer is that prompts are suggestions. Infrastructure is enforcement.

A system prompt can be overridden by a long context window, a strongly-worded user message, or accumulated conversational pressure. The Pre-Response Sparring Hook is a hard intercept — it runs at the infrastructure layer before the response is generated, logs its decision, and its verdict is part of the request trace.

This makes it auditable, configurable, and enforceable in a way that a prompt instruction never is.

---

## Trace Output

Every sparring evaluation is recorded in the request trace:

```
ctx_7f3a9b2 → plan_spar
  verdict: PROCEED
  confidence: 0.87
  pattern_matched: "campaign_optimization"
  pattern_differences_noted: 1
  latency: 340ms
  tokens: 412
```

This means you can audit, over time, how often the sparring hook fires, what it catches, and whether its verdicts were correct.

---

*The Pre-Response Sparring Hook was conceived by John Williams (IASAWI) from a practitioner insight about the pattern-matching blind spot in both human operators and AI agents.*
