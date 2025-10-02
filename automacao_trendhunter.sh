#!/bin/bash
# TrendHunter - Automação Completa
# Executado automaticamente via crontab

cd /home/josecicero/Documentos/Clones/AutomatedTrendHunting

echo "🚀 $(date): Iniciando TrendHunter"

# 1. Atualiza tendências
python3 trend_hunter_pro.py

# 2. Executa sistema de monetização
python3 sistema_monetizacao.py

echo "✅ $(date): Automação concluída"
