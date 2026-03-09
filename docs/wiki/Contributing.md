# Contributing to ContextOS

Thank you for wanting to make ContextOS better. This guide covers everything you need to contribute.

---

## Before You Start

Read [Credits and Origins](./Credits-and-Origins.md). ContextOS exists because six projects did great work. Any contribution that touches the integration with those projects should maintain the spirit of gratitude toward them.

---

## What We Need Most

In order of priority:

1. **Integration completions** — the composio, ragflow, and context7 integrations are stubs. Real implementations of these are high priority.
2. **Test coverage** — the core package needs unit and integration tests.
3. **LLM call implementations** — several methods are documented stubs (marked with "Stub: LLM call in production"). Implement them.
4. **Pre-Response Sparring Hook evaluation** — improve the LLM prompt and the verdict logic.
5. **Entity graph NER** — implement the entity extraction pipeline in the memory layer.

---

## Setup

```bash
git clone https://github.com/itallstartedwithaidea/contextOS
cd contextOS
pip install -e ".[dev]"
```

---

## Code Standards

- Python 3.10+ type hints throughout
- Docstrings on all public methods
- `ruff` for linting (`ruff check .`)
- `black` for formatting (`black .`)
- Tests with `pytest`

---

## PR Guidelines

1. One PR per feature or fix
2. Reference the issue your PR addresses
3. Include tests for new functionality
4. Update the relevant wiki page if behavior changes
5. Credit any source repo your PR draws from

---

## Reporting Issues

Use GitHub Issues. Include:
- ContextOS version (`contextos --version`)
- Python version
- What you expected vs what happened
- Minimal reproduction case

---

## Code of Conduct

Be direct. Be respectful. Credit your sources. We're building something useful, not building a reputation.
