# Safety Test Plan

## Objective

Validate that the public static preview remains defensive, local-first, and free of avoidable public security risks.

## Checks

1. Repository scope
   - Confirm public files match `SECURITY_SCOPE.md`.
   - Confirm no private paths, hostnames, account emails, tokens, keys, or raw logs appear in public docs.

2. Static app behavior
   - Review `index.html` for external scripts, unsafe inline handlers, and missing defensive headers where applicable.
   - Review `app.js` for dangerous sinks, dynamic execution, unsafe HTML insertion, storage of sensitive data, and export behavior.
   - Review `styles.css` for external imports or remote resources.

3. Documentation consistency
   - Confirm README links and referenced evidence files exist.
   - Confirm public disclaimers do not overclaim affiliation, certification, or production readiness.

4. Runtime guardrails
   - Confirm `RUNTIME_GUARDRAILS.yaml`, `APPROVAL_GATES.md`, allowlist, denylist, monitoring, and enforcement docs exist.

## Proposed validation commands

Do not execute without approval:

```powershell
rg -n "C:\\Users|file:///|sk-|ghp_|token|password|secret|private key|BEGIN .* KEY" .
rg -n "innerHTML|outerHTML|insertAdjacentHTML|eval\(|Function\(|document.write|localStorage|sessionStorage" app.js index.html
node --check app.js
git diff --check
```
