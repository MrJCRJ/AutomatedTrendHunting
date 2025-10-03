# TrendHunter (Produção)

Plataforma automatizada para descoberta e distribuição de tendências com monetização integrada.

## 🚀 Visão Geral

- Coleta automática de tendências (Google Trends)
- Distribuição multicanal (Newsletter, Telegram, WhatsApp, Push)
- Monetização via Google AdSense
- Infraestrutura automatizada (GitHub Actions)

## 📂 Estrutura

```
automation/          # Scripts de coleta e distribuição
	trend_hunter_pro.py
	sistema_monetizacao.py
	newsletter_mailchimp.py
	telegram_bot.py
	whatsapp_business.py
	diagnostico.py
	teste_visual.py
	trend_hunter.py

public/              # (Reservado para assets estáticos futuros)

docs/                # Documentação detalhada
	README_MONETIZACAO.md
	PRODUCAO_COMPLETA.md
	CONFIGURACAO_APIS.md
	ADSENSE_VERIFICACAO.md
	AUTOMACAO.md
	GUIA_ATUALIZACAO.md

.github/workflows/   # Automação CI/CD e coleta agendada
```

## � Workflows Principais

- `trend-automation.yml` → Executa coleta e monetização a cada 6h
- `deploy.yml` → Deploy automático (Vercel/Netlify)

## 🔐 Secrets Necessárias

Configurar em GitHub → Settings → Secrets → Actions:

```
MAILCHIMP_API_KEY
MAILCHIMP_AUDIENCE_ID
TELEGRAM_BOT_TOKEN
TELEGRAM_CHANNEL_ID
WHATSAPP_ACCESS_TOKEN
WHATSAPP_PHONE_ID
VERCEL_TOKEN (opcional)
VERCEL_ORG_ID (opcional)
VERCEL_PROJECT_ID (opcional)
DASHBOARD_PASSWORD (proteção do dashboard)
DASHBOARD_JWT_SECRET (opcional: assinatura forte)
```

## 📊 Arquivos Públicos / Migração

A aplicação passou por uma simplificação: as páginas HTML estáticas foram descontinuadas nesta fase inicial. O dashboard agora é servido 100% via função serverless.

Removidos / migrados:

- `index.html` → substituído pelo endpoint dinâmico apenas interno
- `dashboard.html` → migrado para `GET /api/dashboard`
- `politica-privacidade.html` → placeholder mínimo (sem conteúdo efetivo por enquanto)

Mantidos (caso precise para compliance / anúncios futuros):

- `ads.txt`
- `robots.txt`
- `sitemap.xml` (pode ser futuramente regenerado por função)

Endpoint do painel agora:

```
GET /api/dashboard
```

Observação: Sem páginas públicas, o projeto está operando em modo “interno / early build”. Quando o marketing/landing voltar, restaurar `index.html` ou introduzir um framework (Next.js) para página pública + painel separado.

## 🔒 Proteção do Dashboard

O dashboard administrativo agora é servido por `GET /api/dashboard` e protegido por senha usando o fluxo `/api/dashboard-auth`.

1. Defina a secret `DASHBOARD_PASSWORD` (ex: "SenhaForte123!") no ambiente do deploy (Vercel ou GitHub Actions se for usar em funções customizadas).
2. (Opcional) Defina `DASHBOARD_JWT_SECRET` para assinatura HMAC diferenciada do valor da senha.
3. Fluxo:

- Usuário acessa `/api/dashboard`
  - Overlay de login solicita senha
  - Front faz `POST /api/dashboard-auth` → retorna token efêmero (1h)
  - Token armazenado em `localStorage` (se "manter logado") ou `sessionStorage`

### Endpoints

Autenticação:

```
POST /api/dashboard-auth
Body: { "password": "<senha>" }
Resposta: { token: "<exp>.<hmac>", expiresIn: 3600 }
```

Dashboard HTML dinâmico:

```
GET /api/dashboard
```

### Renovação de Sessão

No momento não há refresh; após expirar (1h) o overlay volta a aparecer.

### Endurecimento Futuro (Sugestões)

- Rate limiting básico (ex: armazenar contagem de tentativas em KV / Edge Config)
- Bloqueio por IP após X falhas
- Migrar para provider de auth (Clerk, Auth0) se escalar
- Adicionar verificação do token em endpoints adicionais (se expostos no futuro)

## 🛠 Manutenção

Scripts auxiliares (ex: `configurador.py`, `monitor_producao.py`) podem ser movidos depois para `tools/` se ainda forem necessários localmente. Não são exigidos em produção.

## 📘 Documentação

Leia em `docs/`:

- `PRODUCAO_COMPLETA.md` – Guia de produção
- `README_MONETIZACAO.md` – Estratégia de monetização
- `CONFIGURACAO_APIS.md` – Setup seguro
- `ADSENSE_VERIFICACAO.md` – Checklist AdSense

## ✅ Status Atual

Modo interno consolidado (arquitetura 100% serverless para UI + APIs). Implementado:

- Dashboard dinâmico (`GET /api/dashboard`)
- Autenticação com token efêmero (`POST /api/dashboard-auth`)
- Rate limiting básico em memória (5 tentativas inválidas / 5min) na autenticação
- Estatísticas persistidas em JSON (`/api/stats` + utilitários internos)
- Endpoints de simulação operacional:
  - `POST /api/executar-tendencias` → incrementa `totalTrends` (1–3)
  - `POST /api/monetizar` → incrementa `newslettersSent` (+1) e `revenueEstimate` (+5.00)
- Testes automatizados com Jest cobrindo autenticação, rate limit e endpoints operacionais

Próximos marcos sugeridos:

- Reintroduzir landing pública (SEO, captação newsletter)
- Validar token nos endpoints operacionais (hardening)
- Persistência de rate limiting em storage distribuído (KV/Redis) para produção
- Enriquecer `/api/stats` com dados derivados (ex: crescimento semanal)
- Reativar política de privacidade completa antes de abertura pública
- Adicionar alertas (email / webhook) de novas tendências

### Política de Rate Limiting (MVP)

Implementação atual é in-memory por instância (não compartilhada entre lambdas). Configuração fixa:

- Janela: 5 minutos
- Limite: 5 tentativas inválidas (senha incorreta)
- Resposta ao exceder: 401 com mensagem "Too many attempts"
- Header adicional: `Retry-After: 300`

Para produção: migrar para solução distribuída (Upstash Redis, Vercel KV, Cloudflare Turnstile + KV, etc.).

### Endpoints Atuais

```
POST /api/dashboard-auth       # Autenticação (senha -> token curto)
GET  /api/dashboard            # HTML do painel
GET  /api/index                # Página de entrada interna (landing temporária)
GET  /api/stats                # Estatísticas agregadas
POST /api/stats-update         # Atualização manual (x-admin-token)
POST /api/executar-tendencias  # Simular processamento de tendências
POST /api/monetizar            # Simular envio/newsletter & receita
GET  /api/ping                 # Diagnóstico simples
GET  /api/_introspect          # Metadados internos
```

### Testes Automatizados

Executar:

```
npm test
```

Cobertura atual:

- Autenticação: casos de sucesso, falha, ausência de env, rate limiting
- Operacionais: incremento de métricas em `/api/executar-tendencias` e `/api/monetizar`

### Estrutura de Dados (stats.json)

```
{
	totalTrends: number,
	newslettersSent: number,
	premiumSubs: number,
	revenueEstimate: number,
	lastUpdated: string (ISO),
	delta24h?: {
		totalTrends: number,
		newslettersSent: number,
		premiumSubs: number,
		revenueEstimate: number
	}
}
```

### Roadmap Técnico Rápido

1. Validar tokens nos endpoints de mutação (execução / monetização)
2. Migrar rate limit para storage distribuído
3. Adicionar camada de cache para `/api/stats`
4. Criar landing pública otimizada para SEO
5. Introduzir fila/cron real para coleta de tendências
6. Implementar alertas (email / push) de tendências emergentes

---

© 2025 TrendHunter
