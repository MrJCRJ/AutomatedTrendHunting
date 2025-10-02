#!/bin/bash

echo "🔥 TrendHunter - Setup Automático"
echo "================================="
echo ""

# Verifica se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Instale Python 3 primeiro."
    exit 1
fi

echo "✅ Python 3 encontrado"

# Instala dependências
echo "📦 Instalando dependências..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependências instaladas com sucesso!"
    echo ""
    echo "🚀 Para atualizar as tendências, execute:"
    echo "   python3 trend_hunter.py"
    echo ""
    echo "⚡ Para automação diária, adicione ao crontab:"
    echo "   0 9 * * * cd $(pwd) && python3 trend_hunter.py"
else
    echo "❌ Erro ao instalar dependências"
    echo "💡 Tente executar manualmente:"
    echo "   pip3 install pytrends requests"
fi