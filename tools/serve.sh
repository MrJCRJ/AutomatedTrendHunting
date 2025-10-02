#!/bin/bash

echo "🔥 TrendHunter MVP - Servidor Local"
echo "=================================="
echo ""
echo "📂 Servindo arquivos do diretório atual..."
echo "🌐 Acesse: http://localhost:8000"
echo ""
echo "Pressione Ctrl+C para parar"
echo ""

# Tenta Python 3 primeiro, depois Python 2
if command -v python3 &> /dev/null; then
    python3 -m http.server 8000
elif command -v python &> /dev/null; then
    python -m http.server 8000
else
    echo "❌ Python não encontrado. Instale Python para testar localmente."
    echo "Ou publique direto no Vercel/Netlify!"
fi