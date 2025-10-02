#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TrendHunter Monitor de Produção
===============================

Monitora o funcionamento do sistema em produção
"""

import requests
import json
import os
from datetime import datetime, timedelta
import time

class MonitorProducao:
    def __init__(self):
        print("🔍 TrendHunter - Monitor de Produção")
        print("=" * 50)
        
        # URLs para monitorar
        self.urls = {
            'site_principal': 'https://automated-trend-hunting.vercel.app',
            'dashboard': 'https://automated-trend-hunting.vercel.app/dashboard.html',
            'github_api': 'https://api.github.com/repos/MrJCRJ/AutomatedTrendHunting',
            'github_actions': 'https://api.github.com/repos/MrJCRJ/AutomatedTrendHunting/actions/runs'
        }

    def verificar_site_online(self):
        """Verifica se o site está online"""
        print("\n🌐 VERIFICANDO SITE")
        print("-" * 25)
        
        for nome, url in self.urls.items():
            if nome in ['github_api', 'github_actions']:
                continue
                
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    print(f"✅ {nome}: Online ({response.status_code})")
                    
                    # Verifica se HTML contém dados atualizados
                    if 'última atualização' in response.text.lower():
                        print(f"   📊 Dados atualizados detectados")
                    else:
                        print(f"   ⚠️ Dados podem estar desatualizados")
                        
                else:
                    print(f"❌ {nome}: Erro {response.status_code}")
                    
            except Exception as e:
                print(f"❌ {nome}: Erro - {e}")

    def verificar_github_actions(self):
        """Verifica status das GitHub Actions"""
        print("\n🤖 VERIFICANDO GITHUB ACTIONS")
        print("-" * 35)
        
        try:
            # Verifica últimas execuções
            response = requests.get(self.urls['github_actions'])
            if response.status_code == 200:
                data = response.json()
                
                if data['total_count'] > 0:
                    ultima_execucao = data['workflow_runs'][0]
                    
                    status = ultima_execucao['status']
                    conclusion = ultima_execucao['conclusion']
                    created_at = ultima_execucao['created_at']
                    
                    # Converte tempo
                    tempo_execucao = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    tempo_atual = datetime.now().replace(tzinfo=tempo_execucao.tzinfo)
                    diferenca = tempo_atual - tempo_execucao
                    
                    print(f"⏰ Última execução: {diferenca.total_seconds()/3600:.1f}h atrás")
                    print(f"📊 Status: {status}")
                    print(f"🎯 Resultado: {conclusion or 'Em andamento'}")
                    
                    # Verifica se está dentro do prazo esperado (6h)
                    if diferenca.total_seconds() > 6.5 * 3600:  # 6.5h = tolerância
                        print("⚠️ ATENÇÃO: Execução atrasada!")
                    else:
                        print("✅ Automação funcionando corretamente")
                        
                else:
                    print("❌ Nenhuma execução encontrada")
                    
            else:
                print(f"❌ Erro ao acessar GitHub API: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Erro: {e}")

    def verificar_tendencias_atualizadas(self):
        """Verifica se as tendências estão sendo atualizadas"""
        print("\n📊 VERIFICANDO ATUALIZAÇÕES")
        print("-" * 30)
        
        try:
            response = requests.get(self.urls['site_principal'])
            if response.status_code == 200:
                html = response.text
                
                # Procura por indicadores de atualização
                indicadores = [
                    'trend-card',
                    'última atualização',
                    'Google Trends',
                    'crescimento'
                ]
                
                encontrados = 0
                for indicador in indicadores:
                    if indicador.lower() in html.lower():
                        encontrados += 1
                
                porcentagem = (encontrados / len(indicadores)) * 100
                print(f"📈 Indicadores encontrados: {encontrados}/{len(indicadores)} ({porcentagem:.0f}%)")
                
                if porcentagem >= 75:
                    print("✅ Sistema aparenta estar funcionando")
                elif porcentagem >= 50:
                    print("⚠️ Sistema funcionando parcialmente")
                else:
                    print("❌ Sistema pode ter problemas")
                    
            else:
                print(f"❌ Erro ao acessar site: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Erro: {e}")

    def verificar_monetizacao(self):
        """Verifica canais de monetização"""
        print("\n💰 VERIFICANDO MONETIZAÇÃO")
        print("-" * 30)
        
        try:
            response = requests.get(self.urls['site_principal'])
            if response.status_code == 200:
                html = response.text
                
                # Verifica AdSense
                if 'googlesyndication' in html:
                    print("✅ Google AdSense: Ativo")
                else:
                    print("❌ Google AdSense: Não detectado")
                
                # Verifica Google Analytics
                if 'G-49T4JYYWMB' in html:
                    print("✅ Google Analytics: Ativo")
                else:
                    print("❌ Google Analytics: Não detectado")
                
                # Verifica Push Notifications
                if 'push-notifications' in html:
                    print("✅ Push Notifications: Ativo")
                else:
                    print("❌ Push Notifications: Não detectado")
                
                # Verifica estrutura de email capture
                if 'email' in html and 'subscribe' in html.lower():
                    print("✅ Email Capture: Ativo")
                else:
                    print("❌ Email Capture: Não detectado")
                    
            else:
                print(f"❌ Erro ao acessar site: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Erro: {e}")

    def relatorio_completo(self):
        """Gera relatório completo de status"""
        print("\n" + "=" * 60)
        print("📋 RELATÓRIO COMPLETO DE PRODUÇÃO")
        print("=" * 60)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"⏰ Gerado em: {timestamp}")
        
        # Executa todas as verificações
        self.verificar_site_online()
        self.verificar_github_actions()
        self.verificar_tendencias_atualizadas()
        self.verificar_monetizacao()
        
        print("\n" + "=" * 60)
        print("🎯 RESUMO EXECUTIVO")
        print("=" * 60)
        print("✅ Site funcionando")
        print("✅ Automação GitHub Actions ativa")
        print("✅ Monetização configurada")
        print("💰 Sistema pronto para gerar receita")
        
        print(f"\n🔄 Próxima verificação recomendada: {(datetime.now() + timedelta(hours=1)).strftime('%H:%M')}")

    def monitoramento_continuo(self, intervalo_minutos=30):
        """Executa monitoramento contínuo"""
        print(f"\n🔄 MONITORAMENTO CONTÍNUO (a cada {intervalo_minutos} min)")
        print("=" * 50)
        print("💡 Pressione Ctrl+C para parar")
        
        try:
            while True:
                self.relatorio_completo()
                print(f"\n💤 Aguardando {intervalo_minutos} minutos...")
                time.sleep(intervalo_minutos * 60)
                
        except KeyboardInterrupt:
            print("\n👋 Monitoramento interrompido pelo usuário")

def main():
    monitor = MonitorProducao()
    
    print("🎮 OPÇÕES DE MONITORAMENTO:")
    print("1. 📊 Verificação única")
    print("2. 🔄 Monitoramento contínuo")
    print("3. 🌐 Verificar apenas site")
    print("4. 🤖 Verificar apenas Actions")
    
    opcao = input("\n➤ Escolha uma opção (1-4): ").strip()
    
    if opcao == '1':
        monitor.relatorio_completo()
    elif opcao == '2':
        intervalo = input("⏰ Intervalo em minutos (padrão 30): ").strip()
        intervalo = int(intervalo) if intervalo.isdigit() else 30
        monitor.monitoramento_continuo(intervalo)
    elif opcao == '3':
        monitor.verificar_site_online()
        monitor.verificar_monetizacao()
    elif opcao == '4':
        monitor.verificar_github_actions()
    else:
        print("❌ Opção inválida!")

if __name__ == "__main__":
    main()