# GitHub Project V2 UI Setup

## Purpose

This document is the manual fallback for creating the GitHub Project V2 board when automation is unavailable, `gh` is not installed, authentication is missing, or the available token lacks Project V2 permissions.

## Target project

Title:

```text
FCCSecurity Public Release Gate
```

Description:

```text
Operational board for tracking defensive findings, validation evidence, remediation status, residual risk, rollback notes, and public-release readiness for FCCSecurity-Public.
```

Repository:

```text
aisamuraiagent-source/FCCSecurity-Public
```

## Manual UI steps

1. Open the repository in GitHub.
2. Go to `Projects`.
3. Select `New project`.
4. Choose a table or board layout.
5. Set title to `FCCSecurity Public Release Gate`.
6. Add the description above.
7. Add or link the repository `aisamuraiagent-source/FCCSecurity-Public`.
8. Add issues:
   - #6 Add automated static/security regression workflow
   - #7 Validate public release documentation does not expose local paths
   - #8 Confirm README claims are factual and evidence-backed
   - #9 Maintain evidence manifest for public artifacts
   - #10 Review residual risk before public portfolio use
9. Create or configure the status values below.
10. Create the custom fields below.
11. Apply the initial issue mapping.

## Status values

```text
Backlog
In Validation
Evidence Required
Remediation Planned
Validated
Closed
```

## Custom fields

| Field | Values / purpose |
|---|---|
| Status | Backlog, In Validation, Evidence Required, Remediation Planned, Validated, Closed |
| Priority | P1, P2, P3, P4 |
| Risk Level | Critical, High, Medium, Low, Informational |
| Evidence Hash | SHA-256 or manifest reference |
| Affected Area | README, docs, workflow, public page, evidence artifact, dependency, claim |
| Validation Method | Static review, manual review, CI workflow, hash verification, content diff, screenshot review |
| Counterevidence | What would disprove or weaken the current claim |
| Rollback | Safe reversion path |
| Public Release Gate | Required, Optional, Blocked, Passed |

## Initial mapping

| Issue | Initial status | Priority | Risk level | Public Release Gate |
|---|---|---|---|---|
| #6 | Remediation Planned | P2 | Medium | Required |
| #7 | Evidence Required | P2 | Medium | Required |
| #8 | Evidence Required | P2 | Medium | Required |
| #9 | In Validation | P2 | Medium | Required |
| #10 | Backlog | P2 | Medium | Required |

## Completion rule

Do not move an issue to `Closed` only because the Project board exists. Move only after acceptance criteria, evidence, counterevidence, residual risk, and rollback are reviewed.

## Rollback

If the Project becomes noisy or inaccurate:

- archive the Project view;
- remove incorrect fields;
- unlink issues from the Project;
- keep the GitHub issues and repository files intact;
- document the reason in the relevant issue before closing or changing status.
