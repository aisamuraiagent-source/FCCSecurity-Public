# Security Findings

Status baseline: 2026-06-21.

| ID | Severity | Status | Area | Description | Evidence | Recommended fix | Validation | Residual risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FCCSEC-PUB-001 | MEDIUM | Mitigated | Documentation | README referenced security evidence paths that were absent from the public repository. | GitHub fetch returned 404 for referenced docs before this documentation pass. | Add referenced docs and keep README evidence paths current. | Fetch each referenced path from `main`. | Docs can drift again without regression checks. |
| FCCSEC-PUB-002 | MEDIUM | Mitigated | Governance | Repository lacked persistent `AGENTS.md` defensive operating rules. | `AGENTS.md` was not present before this pass. | Add repo-scoped `AGENTS.md`. | Fetch `AGENTS.md` from `main`. | Future agents must follow it. |
| FCCSEC-PUB-003 | LOW | Open | Testing | No CI/security regression workflow is documented for the public static preview. | No workflow review was performed in this pass. | Add non-network static checks when CI changes are approved. | Proposed commands in `SAFETY_TEST_PLAN.md`. | Manual validation remains required. |
| FCCSEC-PUB-004 | LOW | Open | Runtime data handling | Static local state/export features must not be used with real secrets or sensitive logs. | README states example local data only. | Keep warnings and sanitization rules visible in docs. | Review app copy and export behavior before release changes. | Users can still paste sensitive data manually. |
