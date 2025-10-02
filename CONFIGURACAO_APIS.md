# 🔐 Configuração Segura das APIs

## ⚠️ IMPORTANTE: Configuração de Secrets

Para proteger suas API keys, este projeto usa arquivos de configuração locais que **NÃO são commitados** no Git.

## 🚀 Setup Rápido

### 1. Copie os arquivos de exemplo:
```bash
cp config_mailchimp.json.example config_mailchimp.json
cp config_telegram.json.example config_telegram.json  
cp config_whatsapp.json.example config_whatsapp.json
cp config_adsense.json.example config_adsense.json
```

### 2. Configure suas API keys:
```bash
# Use o configurador automático
python3 configurador.py

# OU edite manualmente os arquivos config_*.json
```

## 📋 APIs Necessárias

### 📧 Mailchimp (Newsletter)
1. Acesse: https://mailchimp.com/
2. Faça login → Profile → Extras → API Keys
3. Copie a API key para `config_mailchimp.json`

### 📱 Telegram Bot
1. Fale com @BotFather no Telegram
2. Use `/newbot` para criar seu bot
3. Copie o token para `config_telegram.json`

### 💎 WhatsApp Business
1. Acesse: https://developers.facebook.com/
2. Crie app WhatsApp Business
3. Configure webhook e obtenha access token
4. Copie para `config_whatsapp.json`

### 💰 Google AdSense
1. Acesse: https://www.google.com/adsense/
2. Adicione seu site e aguarde aprovação
3. Copie Publisher ID para `config_adsense.json`

## 🔒 Segurança

✅ **Arquivos config_*.json são ignorados pelo Git**
✅ **Suas API keys ficam apenas localmente**
✅ **Exemplos seguros estão no repositório**

## 🧪 Teste

```bash
# Teste se está tudo configurado
python3 sistema_monetizacao.py

# Acesse o dashboard
open dashboard.html
```