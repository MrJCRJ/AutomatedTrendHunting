#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste Visual - Mostra ANTES e DEPOIS da atualização
===================================================
"""

from datetime import datetime
import hashlib
import sys
import os

def mostrar_tendencias_atuais():
    """Mostra as tendências que estão no HTML agora"""
    print("📊 TENDÊNCIAS ATUAIS NO SITE:")
    print("=" * 50)
    
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        import re
        # Extrai tendências com mais detalhes
        pattern = r'<h3 class="trend-title">(.*?)</h3>.*?<span class="trend-growth">(.*?)</span>.*?<span class="trend-category">(.*?)</span>'
        matches = re.findall(pattern, conteudo, re.DOTALL)
        
        if matches:
            for i, (titulo, crescimento, categoria) in enumerate(matches, 1):
                print(f"  {i}. {titulo.strip()}")
                print(f"     💹 {crescimento.strip()} | 🏷️ {categoria.strip()}")
                print()
        else:
            print("  ❌ Nenhuma tendência encontrada no HTML")
            
        return len(matches)
        
    except Exception as e:
        print(f"❌ Erro ao ler HTML: {e}")
        return 0

def atualizar_com_dados_novos():
    """Atualiza com dados completamente novos para mostrar diferença"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    # Tendências TOTALMENTE novas para mostrar que realmente mudou
    tendencias_novas = [
        {
            'termo': f'🔥 TESTE REAL {timestamp}',
            'categoria': 'Tecnologia',
            'crescimento': 999,
            'descricao': f'Esta tendência foi criada ÀS {timestamp} para provar que a automação FUNCIONA de verdade!'
        },
        {
            'termo': 'Realidade Virtual para Educação',
            'categoria': 'Tecnologia', 
            'crescimento': 350,
            'descricao': 'Escolas brasileiras adotando VR para ensino. Mercado de R$ 500 milhões até 2025.'
        },
        {
            'termo': 'Criptomoedas Brasileiras',
            'categoria': 'Finanças',
            'crescimento': 280,
            'descricao': 'Tokens nacionais ganhando força. Oportunidade em exchanges e carteiras digitais.'
        },
        {
            'termo': 'Food Delivery Saudável', 
            'categoria': 'E-commerce',
            'crescimento': 210,
            'descricao': 'Alimentação saudável on-demand explodindo pós-pandemia. Nicho premium aquecido.'
        },
        {
            'termo': 'Coworking para Gamers',
            'categoria': 'Casa',
            'crescimento': 190,
            'descricao': 'Espaços compartilhados para streamers e gamers. Novo modelo de negócio emergente.'
        }
    ]
    
    print(f"🚀 ATUALIZANDO COM DADOS NOVOS ({timestamp}):")
    print("=" * 50)
    
    for i, t in enumerate(tendencias_novas, 1):
        print(f"  {i}. {t['termo']}")
        print(f"     💹 +{t['crescimento']}% | 🏷️ {t['categoria']}")
        print()
    
    # Gera cards HTML
    def gerar_card_html(tendencia):
        return f'''        <div class="trend-card">
          <h3 class="trend-title">{tendencia['termo']}</h3>
          <span class="trend-growth">+{int(tendencia['crescimento'])}%</span>
          <span class="trend-category">{tendencia['categoria']}</span>
          <p class="trend-description">
            {tendencia['descricao']}
            <strong>Potencial:</strong> Alto crescimento nos próximos meses.
          </p>
        </div>'''
    
    cards_html = '\n\n'.join([gerar_card_html(t) for t in tendencias_novas])
    
    try:
        # Lê HTML atual
        with open('index.html', 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        # Faz substituição
        inicio_marker = '<h2 style="margin-bottom: 2rem; text-align: center">'
        fim_marker = '</div>\n    </main>'
        
        inicio_idx = conteudo.find(inicio_marker)
        fim_idx = conteudo.find(fim_marker, inicio_idx)
        
        if inicio_idx != -1 and fim_idx != -1:
            novo_conteudo = (
                conteudo[:inicio_idx] +
                f'<h2 style="margin-bottom: 2rem; text-align: center">\n          📈 Tendências em Alta (ATUALIZADO {timestamp})\n        </h2>\n\n' +
                cards_html + '\n\n        ' +
                conteudo[fim_idx:]
            )
            
            # Salva HTML atualizado
            with open('index.html', 'w', encoding='utf-8') as f:
                f.write(novo_conteudo)
            
            print("✅ HTML ATUALIZADO COM SUCESSO!")
            
            # Salva backup
            import json
            timestamp_file = datetime.now().strftime("%Y%m%d_%H%M%S")
            os.makedirs('backups', exist_ok=True)
            with open(f'backups/teste_visual_{timestamp_file}.json', 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': timestamp_file,
                    'tipo': 'teste_visual',
                    'tendencias': tendencias_novas
                }, f, ensure_ascii=False, indent=2)
            
            return True
        else:
            print("❌ Erro: Não conseguiu encontrar marcadores")
            return False
            
    except Exception as e:
        print(f"❌ Erro durante atualização: {e}")
        return False

def main():
    print("🔥 TrendHunter - Teste Visual ANTES/DEPOIS")
    print("=" * 80)
    
    print("\n📋 ANTES DA ATUALIZAÇÃO:")
    qtd_antes = mostrar_tendencias_atuais()
    
    input("\n⏸️  Pressione ENTER para atualizar as tendências...")
    
    print("\n🔄 PROCESSANDO ATUALIZAÇÃO...")
    sucesso = atualizar_com_dados_novos()
    
    if sucesso:
        print("\n📋 DEPOIS DA ATUALIZAÇÃO:")
        qtd_depois = mostrar_tendencias_atuais()
        
        print("=" * 80)
        print("🎉 RESULTADO:")
        print(f"   📊 Antes: {qtd_antes} tendências")
        print(f"   📊 Depois: {qtd_depois} tendências") 
        print("   ✅ HTML foi modificado com SUCESSO!")
        print("\n💡 Próximos passos:")
        print("   1. Acesse seu site para ver as mudanças")
        print("   2. git add . && git commit -m 'Teste visual' && git push")
        print("   3. As mudanças estarão online em poucos minutos")
    else:
        print("❌ Falha na atualização")

if __name__ == "__main__":
    main()