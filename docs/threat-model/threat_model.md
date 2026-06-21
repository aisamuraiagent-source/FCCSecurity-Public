# Threat Model - FCCSecurity-Public

## System summary

`FCCSecurity-Public` is a public sanitized static preview. It is documented as having no backend, database, login, external API, telemetry, credential collection, or production automation.

## Assets

- Public static source files.
- Public documentation and evidence.
- User trust in public claims and disclaimers.
- Local-only example data shown in the browser.

## Trust boundaries

- Browser runtime boundary: static HTML/CSS/JS executes in the user's browser.
- Repository boundary: public GitHub content can be viewed and cloned by anyone.
- Human approval boundary: impactful actions require explicit approval.

## Primary risks

- Public documentation drift or overclaiming.
- Accidental publication of private paths, tokens, hostnames, private IPs, account email, screenshots, or raw logs.
- Future introduction of external scripts, APIs, login, telemetry, or persistence without updating scope.
- Unsafe DOM sinks or dynamic execution in static JavaScript.
- Users pasting sensitive data into local example fields or exports.

## Controls

- `AGENTS.md` for defensive operating rules.
- `SECURITY.md` and `SECURITY_SCOPE.md` for scope and public handling.
- `RUNTIME_GUARDRAILS.yaml` for runtime safety boundary.
- `SAFETY_TEST_PLAN.md` for proposed validation.
- `SECURITY_FINDINGS.md` and `REMEDIATION_BACKLOG.md` for tracked risk.
