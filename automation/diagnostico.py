#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnóstico TrendHunter - Verificar se automação está funcionando
================================================================
"""

import json
import os
from datetime import datetime, timedelta
import hashlib

def verificar_estrutura_html():
    """Verifica a estrutura atual do HTML"""
    print("🔍 DIAGNÓSTICO: Verificando estrutura do HTML")
    print("=" * 60)
    
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        # Procura por marcadores
        marcadores = [
            '<h2 style="margin-bottom: 2rem; text-align: center">',
            '📈 Tendências em Alta',
            'trend-card',
            'trend-title',
            '</div>\n    </main>'
        ]
        
        print("📋 Marcadores encontrados:")
        for marcador in marcadores:
            if marcador in conteudo:
                posicao = conteudo.find(marcador)
                print(f"  ✅ '{marcador}' - Posição: {posicao}")
            else:
                print(f"  ❌ '{marcador}' - NÃO ENCONTRADO")
        
        # Conta tendências atuais
        import re
        titulos = re.findall(r'<h3 class="trend-title">(.*?)</h3>', conteudo)
        print(f"\n📊 Tendências encontradas ({len(titulos)}):")
        for i, titulo in enumerate(titulos, 1):
            print(f"  {i}. {titulo}")
        
        return titulos
        
    except Exception as e:
        print(f"❌ Erro ao ler HTML: {e}")
        return []

def verificar_backups():
    """Verifica se backups estão sendo criados"""
    print("\n💾 DIAGNÓSTICO: Verificando backups")
    print("=" * 60)
    
    if not os.path.exists('backups'):
        print("❌ Pasta 'backups' não existe")
        return []
    
    backups = [f for f in os.listdir('backups') if f.endswith('.json')]
    backups.sort(reverse=True)  # Mais recente primeiro
    
    print(f"📁 Backups encontrados ({len(backups)}):")
    for backup in backups[:5]:  # Mostra os 5 mais recentes
        try:
            caminho = f'backups/{backup}'
            with open(caminho, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            timestamp = dados.get('timestamp', 'N/A')
            tipo = dados.get('tipo', 'automático')
            qtd_tendencias = len(dados.get('tendencias', []))
            
            print(f"  📄 {backup}")
            print(f"     🕒 {timestamp} | 🏷️ {tipo} | 📊 {qtd_tendencias} tendências")
        except Exception as e:
            print(f"  ❌ {backup} - Erro: {e}")
    
    return backups

def verificar_scripts():
    """Verifica se scripts existem e estão executáveis"""
    print("\n🔧 DIAGNÓSTICO: Verificando scripts")
    print("=" * 60)
    
    scripts = [
        'trend_hunter.py',
        'manual_update.py', 
        'demo_manual.py',
        'setup.sh'
    ]
    
    for script in scripts:
        if os.path.exists(script):
            stats = os.stat(script)
            executavel = bool(stats.st_mode & 0o111)
            tamanho = stats.st_size
            
            print(f"  ✅ {script}")
            print(f"     📏 {tamanho} bytes | {'🏃 Executável' if executavel else '⛔ Não executável'}")
        else:
            print(f"  ❌ {script} - NÃO EXISTE")

def verificar_crontab():
    """Verifica configuração do crontab"""
    print("\n⏰ DIAGNÓSTICO: Verificando crontab")
    print("=" * 60)
    
    try:
        import subprocess
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        
        if result.returncode == 0:
            linhas = result.stdout.strip().split('\n')
            trendhunter_jobs = [l for l in linhas if 'trend_hunter.py' in l and not l.startswith('#')]
            
            if trendhunter_jobs:
                print("  ✅ Crontab configurado para TrendHunter:")
                for job in trendhunter_jobs:
                    print(f"     📅 {job}")
            else:
                print("  ⚠️ Crontab existe mas não tem jobs do TrendHunter")
                print("  💡 Execute: crontab crontab_trendhunter")
        else:
            print("  ❌ Nenhum crontab configurado")
            print("  💡 Execute: crontab crontab_trendhunter")
            
    except Exception as e:
        print(f"  ❌ Erro ao verificar crontab: {e}")

def testar_atualizacao_real():
    """Testa se consegue atualizar o HTML de verdade"""
    print("\n🧪 TESTE: Atualizando HTML com dados de teste")
    print("=" * 60)
    
    # Dados de teste únicos
    timestamp = datetime.now().strftime("%H:%M:%S")
    tendencias_teste = [
        {
            'termo': f'Teste de Automação {timestamp}',
            'categoria': 'Tecnologia',
            'crescimento': 999,
            'descricao': f'Esta é uma tendência de teste criada às {timestamp} para verificar se a automação está funcionando.'
        }
    ]
    
    # Salva estado atual
    with open('index.html', 'r', encoding='utf-8') as f:
        html_original = f.read()
    
    hash_original = hashlib.md5(html_original.encode()).hexdigest()
    print(f"📋 Hash do HTML original: {hash_original[:8]}...")
    
    try:
        # Importa e executa função de atualização
        import sys
        sys.path.append('.')
        
        # Simula atualização
        from demo_manual import gerar_card_html
        
        card_teste = gerar_card_html(tendencias_teste[0])
        print(f"🎨 Card gerado: {card_teste[:50]}...")
        
        # Tenta atualizar
        inicio_marker = '<h2 style="margin-bottom: 2rem; text-align: center">'
        fim_marker = '</div>\n    </main>'
        
        inicio_idx = html_original.find(inicio_marker)
        fim_idx = html_original.find(fim_marker, inicio_idx)
        
        if inicio_idx != -1 and fim_idx != -1:
            novo_html = (
                html_original[:inicio_idx] +
                '<h2 style="margin-bottom: 2rem; text-align: center">\n          📈 Tendências em Alta (TESTE ' + timestamp + ')\n        </h2>\n\n' +
                card_teste + '\n\n        ' +
                html_original[fim_idx:]
            )
            
            # Salva temporariamente para testar
            with open('index_teste.html', 'w', encoding='utf-8') as f:
                f.write(novo_html)
            
            hash_novo = hashlib.md5(novo_html.encode()).hexdigest()
            print(f"📋 Hash do HTML novo: {hash_novo[:8]}...")
            
            if hash_original != hash_novo:
                print("✅ SUCESSO: HTML foi modificado com sucesso!")
                print(f"📏 Tamanho original: {len(html_original)} chars")
                print(f"📏 Tamanho novo: {len(novo_html)} chars")
                
                # Remove arquivo de teste
                os.remove('index_teste.html')
                return True
            else:
                print("❌ FALHA: HTML não foi modificado")
                return False
        else:
            print("❌ FALHA: Não conseguiu encontrar marcadores no HTML")
            return False
            
    except Exception as e:
        print(f"❌ ERRO durante teste: {e}")
        return False

def main():
    """Executa diagnóstico completo"""
    print("🔥 TrendHunter - Diagnóstico Completo")
    print("=" * 80)
    
    # Executa todos os diagnósticos
    titulos = verificar_estrutura_html()
    backups = verificar_backups()
    verificar_scripts()
    verificar_crontab()
    sucesso_teste = testar_atualizacao_real()
    
    # Resume resultados
    print("\n" + "=" * 80)
    print("📊 RESUMO DO DIAGNÓSTICO")
    print("=" * 80)
    
    status_geral = "✅ FUNCIONANDO" if sucesso_teste else "❌ COM PROBLEMAS"
    print(f"🎯 Status Geral: {status_geral}")
    print(f"📈 Tendências no HTML: {len(titulos)}")
    print(f"💾 Backups disponíveis: {len(backups)}")
    print(f"🧪 Teste de atualização: {'✅ PASSOU' if sucesso_teste else '❌ FALHOU'}")
    
    if not sucesso_teste:
        print("\n💡 PRÓXIMOS PASSOS RECOMENDADOS:")
        print("1. Execute: python3 demo_manual.py")
        print("2. Verifique se houve mudança no index.html")
        print("3. Se não funcionou, há problema na lógica de parsing")
    
    print("\n🔄 Para forçar uma atualização manual:")
    print("   python3 manual_update.py")

if __name__ == "__main__":
    main()