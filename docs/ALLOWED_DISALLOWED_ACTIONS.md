# Allowed and Disallowed Actions

## Allowed with no write impact

- Read repository files inside authorized scope.
- Review static code and documentation.
- Identify missing docs, stale claims, unsafe copy, weak validation, and public evidence leaks.
- Propose patches in diff form.

## Allowed only after explicit approval

- Modify files.
- Create branches, commits, pull requests, or releases.
- Run local commands.
- Access network resources.
- Install packages.
- Update CI/CD.
- Generate public evidence files.

## Disallowed

- Scanning public targets.
- Exploit execution.
- Credential capture or display.
- Token/session abuse.
- Malware, persistence, evasion, or stealth.
- Bypassing authentication or authorization.
- Destructive commands without explicit justification, safer alternative, and approval.
- Hiding or deleting audit traces.

## Default decision

When scope or permission is unclear, stop, state the uncertainty, and request human approval before acting.
