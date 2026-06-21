# Local Validation

## Status

This document records validation expectations for the public static preview. Commands below are proposed and must not be executed without explicit approval.

## Proposed commands

```powershell
rg -n "C:\\Users|file:///|sk-|ghp_|token|password|secret|private key|BEGIN .* KEY" .
rg -n "innerHTML|outerHTML|insertAdjacentHTML|eval\(|Function\(|document.write|localStorage|sessionStorage" app.js index.html
node --check app.js
git diff --check
python -m http.server 4173 --bind 127.0.0.1
```

## Expected result

- No private paths or secret-like tokens in public files.
- No dynamic code execution sinks without documented justification.
- JavaScript syntax check passes.
- Whitespace check passes.
- Local preview binds only to `127.0.0.1`.

## Current limitation

No local command execution was performed in this documentation pass. Runtime validation remains pending explicit approval.
