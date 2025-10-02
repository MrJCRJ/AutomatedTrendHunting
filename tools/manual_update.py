#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Atualizador Manual de Tendências - Versão Simplificada
======================================================

Para quando você quiser adicionar tendências manualmente de forma rápida.
"""

import json
from datetime import datetime
import os

def criar_tendencia_manual():
    """Interface para criar tendência manualmente"""
    print("🔥 TrendHunter - Adição Manual de Tendência")
    print("=" * 50)
    
    # Coleta dados
    termo = input("📊 Nome da tendência: ").strip()
    if not termo:
        print("❌ Nome da tendência é obrigatório")
        return None
        
    categorias = ['Tecnologia', 'E-commerce', 'Finanças', 'Saúde', 'Casa', 'Outro']
    print("\n📂 Categorias disponíveis:")
    for i, cat in enumerate(categorias, 1):
        print(f"  {i}. {cat}")
    
    try:
        cat_idx = int(input("\nEscolha a categoria (1-6): ")) - 1
        categoria = categorias[cat_idx] if 0 <= cat_idx < len(categorias) else 'Outro'
    except:
        categoria = 'Outro'
    
    try:
        crescimento = float(input("📈 Crescimento (ex: 150 para +150%): "))
    except:
        crescimento = 100.0
    
    descricao = input("📝 Descrição/oportunidade (ou Enter para automática): ").strip()
    
    if not descricao:
        descricoes_auto = {
            'Tecnologia': f"Setor de tecnologia em crescimento. Oportunidades em ferramentas, cursos e consultoria para '{termo}'.",
            'E-commerce': f"E-commerce brasileiro aquecido. Oportunidade para produtos relacionados a '{termo}'.",
            'Finanças': f"Mercado financeiro em movimento. Nicho educacional sobre '{termo}' em alta.",
            'Saúde': f"Setor de saúde digital expandindo. Oportunidades em '{termo}' e wellness.",
            'Casa': f"Mercado residencial inovando. '{termo}' em demanda crescente.",
        }
        descricao = descricoes_auto.get(categoria, f"Tendência '{termo}' emergente com potencial de crescimento.")
    
    return {
        'termo': termo,
        'categoria': categoria,
        'crescimento': crescimento,
        'descricao': descricao,
        'adicionado_em': datetime.now().isoformat()
    }

def gerar_card_html(tendencia):
    """Gera HTML do card"""
    return f'''            <div class="trend-card">
                <h3 class="trend-title">{tendencia['termo']}</h3>
                <span class="trend-growth">+{int(tendencia['crescimento'])}%</span>
                <span class="trend-category">{tendencia['categoria']}</span>
                <p class="trend-description">
                    {tendencia['descricao']}
                    <strong>Potencial:</strong> Alto crescimento nos próximos meses.
                </p>
            </div>'''

def listar_tendencias_atuais():
    """Lista as tendências atuais no site"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        # Extrai títulos das tendências existentes
        import re
        pattern = r'<h3 class="trend-title">(.*?)</h3>'
        titulos = re.findall(pattern, conteudo)
        
        print("\n📋 Tendências atuais no site:")
        for i, titulo in enumerate(titulos, 1):
            print(f"  {i}. {titulo}")
        
        return titulos
    except:
        return []

def atualizar_site_manual():
    """Interface principal para atualização manual"""
    print("🚀 TrendHunter - Atualizador Manual")
    print("=" * 40)
    
    # Mostra tendências atuais
    tendencias_atuais = listar_tendencias_atuais()
    
    print("\n🎯 Opções:")
    print("1. Adicionar nova tendência")
    print("2. Substituir todas as tendências")
    print("3. Sair")
    
    try:
        opcao = input("\nEscolha uma opção (1-3): ").strip()
    except:
        opcao = "3"
    
    if opcao == "1":
        # Adicionar nova tendência
        nova = criar_tendencia_manual()
        if nova:
            print(f"\n✅ Tendência '{nova['termo']}' criada!")
            print("💡 Para aplicar no site, execute: python3 trend_hunter.py")
            
            # Salva em arquivo temporário
            os.makedirs('temp', exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            with open(f'temp/nova_tendencia_{timestamp}.json', 'w', encoding='utf-8') as f:
                json.dump(nova, f, ensure_ascii=False, indent=2)
            
            print(f"💾 Salva em: temp/nova_tendencia_{timestamp}.json")
    
    elif opcao == "2":
        # Substituir todas
        print("\n🔄 Vamos criar novas tendências...")
        novas_tendencias = []
        
        for i in range(5):
            print(f"\n--- Tendência {i+1}/5 ---")
            nova = criar_tendencia_manual()
            if nova:
                novas_tendencias.append(nova)
            else:
                break
        
        if novas_tendencias:
            # Atualiza o HTML diretamente
            cards_html = '\n\n'.join([gerar_card_html(t) for t in novas_tendencias])
            
            try:
                with open('index.html', 'r', encoding='utf-8') as f:
                    conteudo = f.read()
                
                # Substitui seção de tendências
                inicio_marker = '<h2 style="margin-bottom: 2rem; text-align: center;">📈 Tendências em Alta (Atualizado hoje)</h2>'
                fim_marker = '</div>\n    </main>'
                
                inicio_idx = conteudo.find(inicio_marker)
                fim_idx = conteudo.find(fim_marker, inicio_idx)
                
                if inicio_idx != -1 and fim_idx != -1:
                    novo_conteudo = (
                        conteudo[:inicio_idx] +
                        inicio_marker + '\n            \n' +
                        cards_html + '\n\n        ' +
                        conteudo[fim_idx:]
                    )
                    
                    with open('index.html', 'w', encoding='utf-8') as f:
                        f.write(novo_conteudo)
                    
                    print("\n🎉 Site atualizado com sucesso!")
                    print("💡 Próximos passos:")
                    print("   git add .")
                    print("   git commit -m 'Atualizar tendências manualmente'")
                    print("   git push origin main")
                    
                    # Salva backup
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    os.makedirs('backups', exist_ok=True)
                    with open(f'backups/manual_{timestamp}.json', 'w', encoding='utf-8') as f:
                        json.dump({
                            'timestamp': timestamp,
                            'tipo': 'manual',
                            'tendencias': novas_tendencias
                        }, f, ensure_ascii=False, indent=2)
                else:
                    print("❌ Erro: Não consegui encontrar a seção de tendências no HTML")
            
            except Exception as e:
                print(f"❌ Erro ao atualizar site: {e}")
    
    else:
        print("👋 Até logo!")

if __name__ == "__main__":
    atualizar_site_manual()