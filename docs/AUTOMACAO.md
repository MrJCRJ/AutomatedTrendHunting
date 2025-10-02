# 🤖 Automação TrendHunter

## ⚡ Status da Automação

### 🏠 Automação Local (Crontab)

- ✅ **Configurado**: Executa diariamente às 9h
- 📁 **Logs**: `logs/cron.log`
- 📋 **Comando**: `crontab -l` para verificar

### ☁️ Automação na Nuvem (GitHub Actions)

- ✅ **Configurado**: `.github/workflows/update-trends.yml`
- ⏰ **Horário**: Diário às 13:00 UTC (9:00 Brasília)
- 🔄 **Execução Manual**: GitHub → Actions → "Atualizar Tendências"

## 🛠️ Comandos Úteis

### Gerenciar Crontab

```bash
# Ver crontab atual
crontab -l

# Editar crontab
crontab -e

# Remover crontab
crontab -r

# Ver logs de execução
tail -f logs/cron.log
```

### Testar Scripts Localmente

```bash
# Script automático (Google Trends)
python3 trend_hunter.py

# Script manual interativo
python3 manual_update.py

# Demo com dados de exemplo
python3 demo_manual.py
```

### Monitorar GitHub Actions

1. Acesse GitHub.com → Seu repositório
2. Clique na aba "Actions"
3. Veja o histórico de execuções
4. Execute manualmente em "Run workflow"

## 📊 Estratégias de Backup

### Automático

- 🤖 **Crontab**: Backup semanal (domingos 18h)
- ☁️ **GitHub**: Histórico completo no repositório
- 💾 **Local**: Pasta `backups/` com JSON timestampado

### Manual

```bash
# Backup completo
tar -czf backup_$(date +%Y%m%d).tar.gz .

# Só dados importantes
cp -r backups/ ~/backup_trendhunter/
```

## 🔧 Troubleshooting

### Crontab não executa

```bash
# Verificar se cron está rodando
systemctl status cron

# Ver logs do sistema
grep CRON /var/log/syslog

# Testar comando manualmente
cd /path/to/AutomatedTrendHunting && python3 trend_hunter.py
```

### GitHub Actions falha

- Verificar se `requirements.txt` está correto
- Confirmar que o repositório tem permissões de escrita
- Checar logs detalhados na aba Actions

### Rate Limit do Google Trends

- ✅ **Automático**: Script usa dados simulados como fallback
- 💡 **Solução**: Use `python3 manual_update.py` para controle total
- ⏰ **Frequência**: Reduza para execução semanal se necessário

## 🎯 Otimizações

### Performance

- 📊 **Cache**: GitHub Actions usa cache de pip
- ⚡ **Fallback**: Dados simulados quando API falha
- 🔄 **Smart Commit**: Só faz commit se houve mudanças

### Monitoramento

- 📈 **Google Analytics**: Monitora visitantes em tempo real
- 📝 **Logs**: Todas execuções são logadas
- 💾 **Backups**: Histórico completo preservado

### Customização

```bash
# Mudar horário do crontab (exemplo: 15h)
crontab -e
# Altere: 0 9 * * * para: 0 15 * * *

# Mudar frequência GitHub Actions
# Edite .github/workflows/update-trends.yml
# Altere cron: '0 13 * * *' para: '0 13 * * 1,3,5' (segunda, quarta, sexta)
```

---

## 📋 **Checklist de Funcionamento**

- [ ] ✅ Crontab instalado (`crontab -l`)
- [ ] ✅ GitHub Actions criado (`.github/workflows/`)
- [ ] ✅ Logs funcionando (`logs/cron.log`)
- [ ] ✅ Backups automáticos (`backups/`)
- [ ] ✅ Scripts testados manualmente
- [ ] ✅ Deploy automático funcionando (Vercel/Netlify)

**🎉 Sistema 100% automatizado e funcional!**
