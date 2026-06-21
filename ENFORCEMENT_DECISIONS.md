# Enforcement Decisions

## Current baseline

| ID | Severity | Decision | Rationale | Status |
| --- | --- | --- | --- | --- |
| FCCSEC-PUB-001 | MEDIUM | Correct | README referenced evidence paths absent from public repo. | Mitigated by adding referenced docs. |
| FCCSEC-PUB-002 | MEDIUM | Correct | Persistent agent governance was absent. | Mitigated by adding `AGENTS.md`. |
| FCCSEC-PUB-003 | LOW | Monitor | Static regression checks are proposed but not yet implemented in CI. | Open. |
| FCCSEC-PUB-004 | LOW | Monitor | Manual user input can still contain sensitive data in local-only examples. | Open. |

## Merge/release rule

Future `HIGH` findings block merge/release until correction and validation. Future `CRITICAL` findings suspend the affected flow until formal human review, correction, validation, and documentation.
