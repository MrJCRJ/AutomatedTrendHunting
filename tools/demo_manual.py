#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo de Atualização Manual - TrendHunter
========================================
"""

import json
from datetime import datetime
import os

# Tendências de exemplo para demonstração
tendencias_demo = [
    {
        'termo': 'IA para Consultórios Médicos',
        'categoria': 'Tecnologia',
        'crescimento': 280,
        'descricao': 'Médicos descobrindo como usar ChatGPT para automatizar prontuários e diagnósticos. Mercado de R$ 800 milhões no Brasil.'
    },
    {
        'termo': 'Dropshipping de Produtos Pet',
        'categoria': 'E-commerce',
        'crescimento': 190,
        'descricao': 'Pet economy explodindo no Brasil. Oportunidade em produtos importados para pets com margens de 300%.'
    },
    {
        'termo': 'Cursos de Day Trade',
        'categoria': 'Finanças',
        'crescimento': 320,
        'descricao': 'Jovens buscando renda extra após pandemia. Mercado educacional de trading movimenta R$ 2 bilhões.'
    },
    {
        'termo': 'Telemedicina para Idosos',
        'categoria': 'Saúde',
        'crescimento': 175,
        'descricao': 'População idosa crescendo 4% ao ano. Soluções digitais de saúde com demanda reprimida.'
    },
    {
        'termo': 'Casa Inteligente Acessível',
        'categoria': 'Casa',
        'crescimento': 245,
        'descricao': 'Classe média descobrindo automação residencial. Soluções IoT brasileiras com preço competitivo.'
    }
]

def gerar_card_html(tendencia):
    """Gera HTML do card"""
    return f'''        <div class="trend-card">
          <h3 class="trend-title">{tendencia['termo']}</h3>
          <span class="trend-growth">+{int(tendencia['crescimento'])}%</span>
          <span class="trend-category">{tendencia['categoria']}</span>
          <p class="trend-description">
            {tendencia['descricao']}
            <strong>Potencial:</strong> Alto crescimento nos próximos meses.
          </p>
        </div>'''

def atualizar_html_demo():
    """Atualiza o HTML com as tendências demo"""
    print("🔥 TrendHunter - Demo de Atualização Manual")
    print("=" * 50)
    
    print("📊 Tendências que serão adicionadas:")
    for i, t in enumerate(tendencias_demo, 1):
        print(f"  {i}. {t['termo']} ({t['categoria']}) - +{t['crescimento']}%")
    
    # Gera cards HTML
    cards_html = '\n\n'.join([gerar_card_html(t) for t in tendencias_demo])
    
    try:
        # Lê arquivo atual
        with open('index.html', 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        # Encontra seção de tendências
        inicio_marker = '<h2 style="margin-bottom: 2rem; text-align: center">'
        fim_marker = '</div>\n    </main>'
        
        inicio_idx = conteudo.find(inicio_marker)
        fim_idx = conteudo.find(fim_marker, inicio_idx)
        
        if inicio_idx != -1 and fim_idx != -1:
            # Substitui conteúdo
            novo_conteudo = (
                conteudo[:inicio_idx] +
                '<h2 style="margin-bottom: 2rem; text-align: center">\n          📈 Tendências em Alta (Atualizado hoje)\n        </h2>\n\n' +
                cards_html + '\n\n        ' +
                conteudo[fim_idx:]
            )
            
            # Salva arquivo
            with open('index.html', 'w', encoding='utf-8') as f:
                f.write(novo_conteudo)
            
            print("\n✅ HTML atualizado com tendências demo!")
            
            # Salva backup
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            os.makedirs('backups', exist_ok=True)
            with open(f'backups/demo_{timestamp}.json', 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': timestamp,
                    'tipo': 'demo_manual',
                    'tendencias': tendencias_demo
                }, f, ensure_ascii=False, indent=2)
            
            print(f"💾 Backup salvo: backups/demo_{timestamp}.json")
            print("\n🎉 Demo concluída com sucesso!")
            print("💡 Para fazer commit:")
            print("   git add .")
            print("   git commit -m 'Demo: Atualizar tendências manualmente'")
            print("   git push origin main")
            
            return True
        else:
            print("❌ Erro: Não consegui encontrar a seção de tendências no HTML")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao atualizar HTML: {e}")
        return False

if __name__ == "__main__":
    atualizar_html_demo()