# Tool Permission Matrix

| Tool/action class | Default | Approval required | Notes |
| --- | --- | --- | --- |
| Read repository files | Allowed | No, when in scope | Do not read secrets or private files outside scope. |
| Search repository text | Allowed | No, when in scope | Use for static review and evidence mapping. |
| GitHub read-only metadata | Restricted | Yes | Network access requires explicit approval. |
| GitHub write operations | Blocked | Yes | Branch, commit, PR, merge, release, and delete require approval. |
| Local shell commands | Blocked | Yes | Propose commands first; run only after approval. |
| Package install | Blocked | Yes | Avoid unless necessary and approved. |
| CI/CD edits | Blocked | Yes | Treat as high-impact. |
| Secret access | Blocked | Yes | Do not display or log secrets. |
| Destructive actions | Blocked | Yes | Require justification, safe alternative, and rollback notes. |

Minimum privilege applies to every tool call.
