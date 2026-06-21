# Enforcement Decisions

## Current baseline

| ID | Severity | Decision | Rationale | Status |
| --- | --- | --- | --- | --- |
| FCCSEC-PUB-001 | MEDIUM | Correct | README referenced evidence paths absent from public repo. | Mitigated by adding referenced docs. |
| FCCSEC-PUB-002 | MEDIUM | Correct | Persistent agent governance was absent. | Mitigated by adding `AGENTS.md`. |
| FCCSEC-PUB-003 | LOW | Monitor | Static regression checks are proposed but not yet implemented in CI. | Open. |
| FCCSEC-PUB-004 | LOW | Monitor | Manual user input can still contain sensitive data in local-only examples. | Open. |
| FCCSEC-PUB-005 | MEDIUM | Correct | Guardrail validation fails if required governance artifacts are absent. | Mitigated by canonical `docs/` packet plus root mirrors. |
| FCCSEC-PUB-006 | MEDIUM | Correct | Repository secret exposure reports must remain accepted without raw secret values. | Mitigated by policy wording update. |
| FCCSEC-PUB-007 | MEDIUM | Correct | Raw Git remote logging can disclose embedded credentials. | Mitigated by redacted remote guidance. |
| FCCSEC-PUB-008 | MEDIUM | Correct | Release gate should not require unshipped evidence files. | Mitigated by committed `docs/` paths and README update. |
| FCCSEC-PUB-009 | MEDIUM | Correct | Noisy secret scan can create false-positive fatigue. | Mitigated by high-confidence checks and split hygiene scan. |

## Merge/release rule

Future `HIGH` findings block merge/release until correction and validation. Future `CRITICAL` findings suspend the affected flow until formal human review, correction, validation, and documentation.
