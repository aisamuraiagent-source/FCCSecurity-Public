# FCC Security

Frontier Cyber Intelligence e um painel local-first para organizar sinais defensivos, threat model, validacao e evidencia operacional com Codex.

Estado atual: prototipo estatico executavel. Nao ha backend, banco, login, API externa, dependencia de build ou telemetria.

## Como executar

Abra `index.html` diretamente no navegador ou sirva a pasta localmente:

```powershell
python -m http.server 4173 --bind 127.0.0.1
```

Depois acesse:

```text
http://127.0.0.1:4173/
```

## Superficies

- `index.html`: estrutura da interface.
- `styles.css`: sistema visual responsivo.
- `app.js`: dados locais, estado, filtros, selecao de sinais, ledger e exportacao.
- `docs/threat-model/threat_model.md`: threat model base para Codex Security.
- `docs/evidence/implementation_evidence.md`: inventario da primeira entrega.
- `docs/validation/local_validation.md`: evidencia de validacao local.

## Codex Security

O scan repo-wide Codex Security foi executado em 2026-06-18 com cobertura sobre runtime, documentacao, threat model e manifestos de deploy. Resultado final: zero findings reportaveis sobreviventes; uma divergencia documental de status foi corrigida e suprimida antes do relatorio final.

## Disclaimer para publicação

FCC Security is an independent local-first defensive security prototype by Renan Raad. It is not affiliated with, endorsed by, or sponsored by OpenAI. References to Codex or Codex Security describe tools/workflows used during local development and review. The project does not perform external scanning, exploitation, credential collection, malware activity, telemetry, or production monitoring.

Relatorios locais:

```text
local-evidence/codex-security-scans/FCCSecurity/no-head_20260618T085508-0300/report.md
local-evidence/codex-security-scans/FCCSecurity/no-head_20260618T085508-0300/report.html
```

## Pacote local

O pacote estatico de entrega deve ser gerado em:

```text
local-evidence/fccsecurity-frontier-cyber-intelligence.zip
```

Manifesto: `docs/deployment/deploy_manifest.md`.

## Estado de publicação

Fonte de verdade: `docs/deployment/deploy_state.json`.

Consulta padrao:

```powershell
.\scripts\get_deploy_state.ps1
.\scripts\validate_release_gate.ps1
.\\scripts\regenerate_release_status_report.ps1
```

Resultado esperado neste ciclo:

```text
Repository: https://github.com/aisamuraiagent-source/FCCSecurity
Visibility: private
Gate status: open
Reason: Checklist release block closed by authorized request; publication remains paused until URL reachability checks pass.
Public URLs: configured (20260621 URL still returns non-reachable status and must return HTTP 200-399)
```

Estado atual detalhado:

- `docs/deployment/release_status_report.md`

## Limites

- Os dados do painel sao exemplos locais para estruturar fluxo defensivo.
- Nao existe ingestao automatica de logs ou alertas reais.
- Nao houve deploy externo nesta etapa.
