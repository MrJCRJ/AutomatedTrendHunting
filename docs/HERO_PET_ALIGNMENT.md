# Alinhamento de Melhorias (AutomatedTrendHunting ↔ Hero-Pet)

Este documento lista melhorias observadas no projeto Hero-Pet que podem ser aplicadas ao AutomatedTrendHunting para elevar organização, manutenção e escalabilidade.

## 1. Organização de Componentes e Domínios

- Separar por domínios (ex: `trends/`, `newsletter/`, `ads/`, `auth/`).
- Adotar convenção semelhante à pasta `components/` do Hero-Pet (subpastas: `common/`, `layout/`, `ui/`).

## 2. Padronização de Formulários e Validação

- Criar camada de validação central (ex: `lib/validation/`).
- Uso de schemas (ex: Zod ou Yup) para entradas de automações: cadastro de fontes, configuração de APIs.

## 3. Hooks Reutilizáveis

Inspirado nos hooks (`usePaginated*`, `useStatus`) do Hero-Pet:

- Criar `useAutomationStatus`, `useAdsMetrics`, `useNewsletterQueue`.

## 4. Logs e Observabilidade

- Adicionar camada `lib/logs.js` com níveis: debug, info, warn, error.
- Padronizar saída em JSON para facilitar ingestão futura.

## 5. Testes

Hero-Pet possui testes organizados por área.
Sugestão:

```
/tests
  /api
  /automation
  /jobs
  /integrations
  /utils
```

Priorizar testes para: geração de relatórios, coleta de trends, envio de notificações.

## 6. Estrutura de Rotas / API

- Adicionar doc de cada endpoint (similar ao `dashboard-auth`).
- Padronizar respostas: `{ success, data, error }`.

## 7. Configurações Externas

Arquivos exemplo já existem (`config_*.json.example`). Criar script de verificação:

```
node scripts/check-configs.js
```

Valida presença e formato dos arquivos reais.

## 8. Automação e Filas

Avaliar introdução futura de uma fila leve (ex: BullMQ ou Redis Streams). Inicialmente, manter FIFO simples em memória/disco.

## 9. Documentação de Fluxos

Criar docs adicionais:

- `docs/FLUXO_TREND_COLETA.md`
- `docs/FLUXO_NOTIFICACOES.md`
- `docs/FLUXO_MONETIZACAO.md`

## 10. Padronização de Estilo

Adicionar `CODE_STYLE.md` (já existe no Hero-Pet) com convenções replicadas aqui.

---

## Próximos Passos Propostos

| Ordem | Item                                          | Impacto |
| ----- | --------------------------------------------- | ------- |
| 1     | Script de checagem de configs                 | Alto    |
| 2     | Padronizar respostas API                      | Médio   |
| 3     | Introduzir camada de logs                     | Alto    |
| 4     | Criar testes básicos para automações críticas | Alto    |
| 5     | Documentar fluxos principais                  | Médio   |
| 6     | Validar inputs com schema                     | Alto    |
| 7     | Organização de pastas por domínio             | Médio   |
| 8     | Hooks internos para métricas/status           | Médio   |
| 9     | Planejar adoção de filas                      | Médio   |
| 10    | Melhorar observabilidade (futuro)             | Médio   |

## Referência Cruzada

- Hero-Pet: organização de componentes, validações e testes → base para modularização.
- AutomatedTrendHunting: foco em automação → precisa robustez operacional e clareza de fluxo.

---

Se quiser, posso já criar o script de checagem de configs e um exemplo de schema de validação. Solicite e avanço na implementação.

---

## Progresso Implementado

- [x] Script `scripts/check-configs.js` criado
- [x] Schemas Zod em `lib/schemas.js`
- [x] Helper padronizado de respostas `lib/apiResponse.js`
- [x] Logger estruturado `lib/log.js`
- [x] Teste inicial `tests/dashboard-auth.test.js` (execução via `npm test`)
- [x] Endpoint alternativo Edge `api/dashboard-auth-edge.js`
- [x] Endpoint de métricas `api/stats.js` e consumo no `dashboard.html`

## Como Usar

```bash
npm install
npm run check:configs   # Valida arquivos de configuração
npm test                # Roda teste do endpoint dashboard-auth
```

Se algum arquivo de config faltar, copie o respectivo `*.example` e ajuste os valores.

## Próximos Itens Recomendados

1. Adicionar testes para `scripts/check-configs.js` cobrindo cenários de erro.
2. Criar endpoint de coleta de trends padronizado usando `automationInputSchema`.
3. Adicionar métricas simples (contagem de execuções + duração) e enrich de logs com `requestId`.
4. Expandir validação para permitir flags de feature (ex: ativar/desativar canais de distribuição).
5. Adicionar pipeline CI rodando `npm test` + `npm run check:configs`.

---

## Node vs Edge (dashboard-auth)

| Aspecto                  | Node (Atual)                         | Edge (Alternativa)                            |
| ------------------------ | ------------------------------------ | --------------------------------------------- |
| Latência                 | Boa                                  | Melhor em regiões distribuídas                |
| Crypto                   | Node `crypto`                        | Web Crypto API                                |
| Cold Start               | Mais perceptível                     | Geralmente menor                              |
| Acesso FS / libs nativas | Disponível                           | Limitado                                      |
| Caso de uso ideal        | Lógica pesada, dependências diversas | Autenticação rápida, caching, geodistribuição |

Escolha: manter Node para máxima compatibilidade; usar Edge se priorizar latência global e simplicidade.

---

## Métricas Implementadas

Endpoints:

- GET `/api/stats` → Retorna métricas validadas (Zod) + `delta24h`.
- POST `/api/stats-update` → Atualiza métricas (header `x-admin-token` deve corresponder a `METRICS_TOKEN`).

Arquivos principais:

- `api/_lib/statsSchema.js` (Zod schema)
- `api/_lib/statsUtil.js` (carregar/salvar/calcular delta + histórico)
- `data/stats.json` (snapshot atual)
- `data/stats-history.json` (gerado automaticamente ao atualizar / salvar deltas)
- `scripts/update-stats.js` (atualização local ou remota)

Formato base:

```json
{
  "totalTrends": 450,
  "newslettersSent": 20,
  "premiumSubs": 25,
  "revenueEstimate": 6000,
  "delta24h": {
    "totalTrends": 47,
    "newslettersSent": 3,
    "premiumSubs": 2,
    "revenueEstimate": 453
  },
  "lastUpdated": "2025-10-02T22:15:00.000Z"
}
```

Uso rápido:

```bash
METRICS_TOKEN=seu_token node scripts/update-stats.js --totalTrends 450 --revenueEstimate 6000
```

Se `METRICS_TOKEN` ou endpoint ausentes → atualização local do `data/stats.json`.

Próximos possíveis incrementos:

1. Guardar também `delta7d` e `delta30d`.
2. Calcular média por hora de `totalTrends`.
3. Expor endpoint `GET /api/stats/history?window=24h`.
4. Adicionar compressão (gzip) em responses maiores.
5. Adicionar testes automatizados para stats-utils.
