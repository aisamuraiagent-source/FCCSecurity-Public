# Corrective Actions

## Completed

- Added repo-scoped `AGENTS.md` defensive operating rules.
- Added public `SECURITY.md` policy.
- Added scope, policy, allowed/disallowed actions, tool permissions, test plan, findings, backlog, runtime guardrails, approval gates, denylist, monitoring, incident, investigation, evidence, enforcement, corrective action, patch validation, and audit evidence files.
- Added README-referenced threat model and local validation documents under `docs/`.

## Proposed next actions

- Add a static CI workflow only after explicit CI/CD approval.
- Run local validation commands only after explicit command execution approval.
- Review UI copy to ensure users are not encouraged to enter real secrets, live logs, or private identifiers.

## Rollback

If public governance wording is considered too broad, update the documentation files with narrower wording instead of deleting audit evidence.
