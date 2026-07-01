# Codex Public Release Gate Agent Rules

## Scope

These rules extend `AGENTS.md` for Public Release Gate work in `FCCSecurity-Public`.

Use this file when the task involves release readiness, public documentation, evidence, residual risk, GitHub Actions, GitHub Project setup, or issues #6 through #10.

## Mandatory sequence

```text
Asset -> Boundary -> Authority Gate -> Intent -> Threat Hypothesis -> Method -> Dry Run -> Execution -> Observation -> Evidence Hash -> Correlation -> Counterevidence -> Risk -> Rollback -> Delivery
```

## Required output structure

1. Diagnostic
2. Plan
3. Execution
4. Evidence
5. Risk / Counterevidence / Rollback
6. Next step

## Defensive-only boundary

Allowed:

- repository-local static review;
- documentation hardening;
- evidence manifest maintenance;
- SHA-256 generation for public artifacts;
- GitHub Actions validation;
- issue/PR/project governance;
- bounded residual-risk review.

Not allowed:

- external scanning;
- exploitation testing;
- credential collection;
- token printing;
- hidden persistence;
- destructive actions;
- claims of complete security;
- unsupported public claims;
- exposing private/local evidence.

## Validation expectation

Before declaring a release-gate task complete, run or document why you could not run:

```bash
python --version
python -m py_compile scripts/public_release_gate_check.py
python scripts/public_release_gate_check.py
git diff --check
```

If `gh` is unavailable or unauthenticated, do not request secrets. Use `docs/GITHUB_PROJECT_UI_SETUP.md` as fallback.

## Evidence expectation

Release-gate evidence should include:

- command/result summary;
- generated report path;
- SHA-256 hash where available;
- issue/PR reference;
- residual-risk decision;
- counterevidence considered;
- rollback path.

## Closure rule

Do not close issues #6 through #10 only because supporting files exist. Close only when each issue has acceptance criteria satisfied with evidence and human review.
