# Residual Risk Note

## Current decision

`Conditional`

## Reason

The public-release gate is being initialized. The scanner, workflow, manifest, residual-risk note, and GitHub Project setup guidance provide structure for evidence and review, but they do not by themselves prove complete security or close the release-gate backlog.

Public use is allowed only with bounded language and without claiming complete security.

## Current scope

In scope:

- repository-local public documentation;
- static GitHub Pages artifact context;
- README claims;
- release-gate documentation;
- generated scanner evidence;
- issues #6 through #10;
- GitHub Actions release-gate workflow.

Out of scope:

- external target scanning;
- third-party system testing;
- credential validation;
- private evidence not committed to this public repository;
- formal audit certification;
- claims of vulnerability absence.

## Open blockers and non-blockers

| Item | Status | Risk decision |
|---|---|---|
| #6 Automated static/security regression workflow | Initialized | Do not close until CI run and artifact are reviewed |
| #7 Public documentation sanitation | Pending review | Do not close until scanner/manual review evidence exists |
| #8 README factual claim review | Pending review | Do not close until claims are mapped to evidence |
| #9 Evidence manifest | Initialized | Keep open until artifact inventory and hashes are reviewed |
| #10 Residual-risk review | Initialized | Keep open until public-use decision is reviewed after workflow run |
| GitHub Project V2 visual board | Manual/automation fallback | Not a security blocker, but useful for governance traceability |

## Counterevidence model

A public-release claim should be weakened, rewritten, or removed if any of the following is observed:

- scanner reports a P1 release blocker;
- public documentation exposes private/local paths or sensitive context;
- README contains unsupported security claims;
- generated evidence is stale or missing;
- CI did not run or artifact is unavailable;
- an issue acceptance criterion is unchecked;
- documentation implies certification, endorsement, or complete security.

## Rollback model

Safe rollback paths:

- revert the release-gate commit;
- disable or adjust `.github/workflows/public-release-gate.yml`;
- remove unsupported public claims;
- remove stale generated evidence;
- reopen issue if evidence becomes stale;
- replace absolute language with bounded language;
- move private evidence out of public scope.

## Public-use rule

Allowed phrasing:

```text
This repository uses a public-release gate to organize validation, evidence, residual-risk review, and rollback notes.
```

Avoid phrasing that implies:

- complete security;
- formal audit;
- vulnerability absence;
- OpenAI endorsement or certification;
- production-grade monitoring or exploitation testing.

## Next review trigger

Review this note after the first successful GitHub Actions run for `Public Release Gate` and after the `public-release-gate-evidence` artifact is inspected.
