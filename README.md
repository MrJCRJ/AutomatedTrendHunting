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
```

## 📊 Arquivos Públicos Relevantes

- `index.html`
- `politica-privacidade.html`
- `ads.txt`
- `robots.txt`
- `sitemap.xml`

## 🛠 Manutenção

Scripts auxiliares (ex: `configurador.py`, `monitor_producao.py`) podem ser movidos depois para `tools/` se ainda forem necessários localmente. Não são exigidos em produção.

## 📘 Documentação

Leia em `docs/`:

- `PRODUCAO_COMPLETA.md` – Guia de produção
- `README_MONETIZACAO.md` – Estratégia de monetização
- `CONFIGURACAO_APIS.md` – Setup seguro
- `ADSENSE_VERIFICACAO.md` – Checklist AdSense

## ✅ Status

Produção pronta para operar 24/7 com automação e monetização ativa.

---

© 2025 TrendHunter
