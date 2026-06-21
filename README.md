# FCC Security

Frontier Cyber Intelligence é um painel local-first para organizar sinais defensivos, threat model, validação e evidência operacional com Codex.

Estado atual: protótipo estático executável. Não há backend, banco, login, API externa, telemetria, coleta de credenciais ou automação de produção.

## Estado de publicação (reconciliado em 2026-06-21)

- Repositório: https://github.com/aisamuraiagent-source/FCCSecurity-Public
- Visibilidade: `public`
- URL pública: https://aisamuraiagent-source.github.io/FCCSecurity-Public/
- Release state: `validated` para preview estático
- Nenhum script de bloqueio de deploy (`public_release_gate`, `deploy_state`, `docs/deployment/private...`) é aplicável no repositório público atual.

## Como executar

Abra `index.html` diretamente no navegador ou sirva a pasta localmente:

```powershell
python -m http.server 4173 --bind 127.0.0.1
```

Depois acesse:

```text
http://127.0.0.1:4173/
```

## Superfícies

- `index.html`: estrutura da interface.
- `styles.css`: sistema visual responsivo.
- `app.js`: dados locais, estado, filtros, sinais, ledger e exportação.
- `docs/threat-model/threat_model.md`: threat model base para revisão defensiva.
- `docs/validation/local_validation.md`: evidência de validação local.
- `docs/security-scans/FCCSecurity/no-head_20260618T085508-0300/report.md`
- `docs/security-scans/FCCSecurity/no-head_20260618T085508-0300/report.html`

## Controles de segurança

O pacote canônico de governança fica em `docs/`. Arquivos equivalentes na raiz são espelhos de compatibilidade para GitHub/PR review.

- `AGENTS.md`: regras operacionais defensivas para agentes Codex neste repositório.
- `SECURITY.md`: política pública de escopo e reporte seguro.
- `docs/SECURITY_SCOPE.md`: ativos em escopo e fora de escopo.
- `docs/SECURITY_POLICY.md`: política defensiva central e critérios de validação.
- `docs/SAFETY_TEST_PLAN.md`: plano de checks propostos, sem execução automática.
- `docs/SAFE_COMMAND_ALLOWLIST.md`: comandos locais permitidos com redaction de remotes.
- `docs/SECURITY_FINDINGS.md`: achados e status de mitigação.
- `docs/REMEDIATION_BACKLOG.md`: backlog de correções e controles pendentes.
- `docs/RUNTIME_GUARDRAILS.yaml`: limites de runtime e gates humanos.
- `docs/PATCH_VALIDATION_REPORT.md`: validação do patch documental.
- `docs/AUDIT_EVIDENCE_PACK.md`: pacote de evidência auditável e sanitizada.

## Disclaimer público

FCC Security é um projeto local-first defensivo e independente de autor.
Não há afiliação, endosso, patrocínio ou parceria com OpenAI.
Referências a Codex/Codex Security descrevem apenas ferramentas e fluxo de revisão usados no desenvolvimento e validação interna.
Não há escaneamento externo automatizado, exploração, abuso de credenciais, malware ou monitoramento operacional.
Os artefatos de segurança deste repositório são evidência documental e não representam certificação, auditoria externa formal ou garantia de ausência de vulnerabilidades.

## Limites

- Os dados do painel são exemplos locais para estruturar fluxo defensivo.
- Não há ingestão automática de logs/alertas reais.
- Não há deploy externo com persistência além do conteúdo estático publicado no GitHub Pages.
