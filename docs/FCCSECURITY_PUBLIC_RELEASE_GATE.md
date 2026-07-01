# FCCSecurity Public Release Gate

## Purpose

This tracker defines the repository-level public-release gate for `FCCSecurity-Public`.

The objective is to keep the public repository defensible as a portfolio artifact: every claim, remediation note, validation statement, and public-facing security assertion should be traceable to observable evidence, bounded scope, residual-risk review, counterevidence, and rollback notes.

## Boundary

In scope:

- repository-local documentation;
- static GitHub Pages artifact context;
- README and public-facing claims;
- GitHub Actions release-gate workflow;
- generated public evidence reports;
- GitHub issues #6 through #10.

Out of scope:

- external target scanning;
- exploitation testing;
- third-party systems;
- credential validation;
- private evidence not sanitized for this public repository;
- claims of complete security or formal audit certification.

## Project board specification

Recommended GitHub Project name:

```text
FCCSecurity Public Release Gate
```

Recommended description:

```text
Operational board for tracking defensive findings, validation evidence, remediation status, residual risk, rollback notes, and public-release readiness for FCCSecurity-Public.
```

Recommended views:

| View | Use |
|---|---|
| Backlog | Candidate work not yet validated |
| In Validation | Work currently being tested or reviewed |
| Evidence Required | Work blocked by missing evidence, hash, manifest, screenshot, log, or source reference |
| Remediation Planned | Confirmed gap with planned corrective action |
| Validated | Evidence exists and claim is currently supportable |
| Closed | Completed or intentionally not pursued with rationale |

Recommended fields:

| Field | Purpose |
|---|---|
| Status | Operational state of the item |
| Priority | P1, P2, P3, or P4 |
| Risk Level | Critical, High, Medium, Low, Informational |
| Evidence Hash | SHA-256 or manifest reference when available |
| Affected Area | README, docs, workflow, public page, evidence artifact, dependency, claim |
| Validation Method | Static review, manual review, CI workflow, hash verification, content diff, screenshot review |
| Counterevidence | What would disprove the claim or weaken confidence |
| Rollback | Safe reversion path |
| Public Release Gate | Required, Optional, Blocked, or Passed |

## Operational sequence

Use this fixed sequence for each tracked item:

```text
Asset -> Boundary -> Authority Gate -> Intent -> Threat Hypothesis -> Method -> Dry Run -> Execution -> Observation -> Evidence Hash -> Correlation -> Counterevidence -> Risk -> Rollback -> Delivery
```

## Issue mapping

| Issue | Purpose | Initial status |
|---|---|---|
| #6 | Add automated static/security regression workflow | Remediation Planned |
| #7 | Validate public release documentation does not expose local paths | Evidence Required |
| #8 | Confirm README claims are factual and evidence-backed | Evidence Required |
| #9 | Maintain evidence manifest for public artifacts | In Validation |
| #10 | Review residual risk before public portfolio use | Backlog |

## Release readiness criteria

The repository is considered public-release ready only when:

- public-facing claims are bounded by explicit scope;
- local/private paths are absent from public documentation;
- evidence artifacts have a manifest or reproducible validation method;
- residual risk is documented instead of hidden;
- any security-related statement is linked to observed evidence or clearly marked as inference;
- rollback exists for material public-facing changes;
- open issues do not contain unresolved P1 release blockers;
- the `Public Release Gate` workflow has run and its artifact has been reviewed.

## Evidence model

Evidence should prefer reproducible artifacts over assertions:

- commit SHA;
- file path and line reference;
- command output;
- CI run result;
- screenshot with capture context;
- manifest JSON;
- SHA-256 hash;
- sanitized report;
- review note with date and scope.

## Counterevidence model

Counterevidence must be recorded when it weakens a claim, including:

- stale evidence;
- workflow failure;
- missing artifact;
- unsupported README claim;
- local/private path exposure;
- ambiguous public wording;
- unresolved P1 release blocker;
- documentation that implies complete security or formal certification.

## Rollback model

Rollback should be documented before public amplification:

- revert commit;
- remove public claim;
- archive outdated artifact;
- replace unsupported statement with bounded language;
- move sensitive/local evidence out of public scope;
- reopen issue if evidence becomes stale;
- disable or adjust workflow if it produces unsafe/noisy evidence.

## Current state

Decision: `Conditional`.

This release-gate tracker has been initialized as repository documentation. The linked issue set should be used as the operational queue for validation, evidence collection, remediation, residual-risk review, and closure.

Do not close issues #6 through #10 until their specific acceptance criteria have evidence and human review.
