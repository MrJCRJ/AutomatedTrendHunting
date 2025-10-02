#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TrendHunter Configuração Rápida
===============================

Script para configurar todas as integrações automaticamente
"""

import json
import os
import sys
from datetime import datetime

class ConfiguradorTrendHunter:
    def __init__(self):
        print("🚀 TrendHunter - Configuração Rápida")
        print("=" * 50)
        
        self.config = {}
        self.apis_configuradas = []

    def banner(self):
        """Exibe banner inicial"""
        print("""
    ████████╗██████╗ ███████╗███╗   ██╗██████╗ 
    ╚══██╔══╝██╔══██╗██╔════╝████╗  ██║██╔══██╗
       ██║   ██████╔╝█████╗  ██╔██╗ ██║██║  ██║
       ██║   ██╔══██╗██╔══╝  ██║╚██╗██║██║  ██║
       ██║   ██║  ██║███████╗██║ ╚████║██████╔╝
       ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═════╝ 
       
    🏆 Sistema de Monetização Automatizada 🏆
        """)

    def configurar_mailchimp(self):
        """Configura integração com Mailchimp"""
        print("\n📧 CONFIGURAÇÃO MAILCHIMP")
        print("-" * 30)
        
        print("1. Acesse: https://mailchimp.com/")
        print("2. Faça login na sua conta")
        print("3. Vá em Profile → Extras → API Keys")
        print("4. Gere uma nova API Key")
        
        api_key = input("\n🔑 Cole sua API Key do Mailchimp: ").strip()
        
        if api_key:
            audience_id = input("📝 ID da sua audiência (opcional): ").strip()
            
            self.config['mailchimp'] = {
                'api_key': api_key,
                'audience_id': audience_id or 'default',
                'ativo': True
            }
            
            # Salva em arquivo específico
            with open('config_mailchimp.json', 'w') as f:
                json.dump({'api_key': api_key, 'audience_id': audience_id}, f)
            
            self.apis_configuradas.append('Mailchimp')
            print("✅ Mailchimp configurado!")
        else:
            print("⚠️ Mailchimp será configurado depois")

    def configurar_telegram(self):
        """Configura bot do Telegram"""
        print("\n📱 CONFIGURAÇÃO TELEGRAM BOT")
        print("-" * 35)
        
        print("1. Abra o Telegram e fale com @BotFather")
        print("2. Digite /newbot")
        print("3. Escolha um nome para seu bot")
        print("4. Escolha um username (deve terminar com 'bot')")
        print("5. Copie o token fornecido")
        
        bot_token = input("\n🤖 Cole o token do seu bot: ").strip()
        
        if bot_token:
            channel_id = input("📢 ID do canal (opcional, ex: @seucanal): ").strip()
            
            self.config['telegram'] = {
                'bot_token': bot_token,
                'channel_id': channel_id or '@trendhunter_alerts',
                'ativo': True
            }
            
            # Salva em arquivo específico
            with open('config_telegram.json', 'w') as f:
                json.dump({'bot_token': bot_token, 'channel_id': channel_id}, f)
            
            self.apis_configuradas.append('Telegram')
            print("✅ Telegram configurado!")
        else:
            print("⚠️ Telegram será configurado depois")

    def configurar_whatsapp(self):
        """Configura WhatsApp Business"""
        print("\n💎 CONFIGURAÇÃO WHATSAPP BUSINESS")
        print("-" * 40)
        
        print("1. Acesse: https://developers.facebook.com/")
        print("2. Crie um app para WhatsApp Business")
        print("3. Configure o webhook")
        print("4. Obtenha o access token")
        
        access_token = input("\n🔐 Access Token do WhatsApp: ").strip()
        
        if access_token:
            phone_id = input("📱 Phone Number ID: ").strip()
            
            self.config['whatsapp'] = {
                'access_token': access_token,
                'phone_number_id': phone_id,
                'ativo': True
            }
            
            # Salva em arquivo específico
            with open('config_whatsapp.json', 'w') as f:
                json.dump({'access_token': access_token, 'phone_number_id': phone_id}, f)
            
            self.apis_configuradas.append('WhatsApp Business')
            print("✅ WhatsApp Business configurado!")
        else:
            print("⚠️ WhatsApp será configurado depois")

    def configurar_google_adsense(self):
        """Configura Google AdSense"""
        print("\n💰 CONFIGURAÇÃO GOOGLE ADSENSE")
        print("-" * 35)
        
        print("1. Acesse: https://www.google.com/adsense/")
        print("2. Faça login com sua conta Google")
        print("3. Adicione seu site")
        print("4. Aguarde aprovação")
        print("5. Copie o código do anúncio")
        
        publisher_id = input("\n🏷️ Seu Publisher ID (ca-pub-xxxxxxx): ").strip()
        
        if publisher_id:
            self.config['adsense'] = {
                'publisher_id': publisher_id,
                'ativo': True
            }
            
            # Salva em arquivo específico
            with open('config_adsense.json', 'w') as f:
                json.dump({'publisher_id': publisher_id}, f)
            
            self.apis_configuradas.append('Google AdSense')
            print("✅ Google AdSense configurado!")
        else:
            print("⚠️ AdSense será configurado depois")

    def configurar_automacao(self):
        """Configura automação completa"""
        print("\n⚙️ CONFIGURAÇÃO DA AUTOMAÇÃO")
        print("-" * 35)
        
        print("Escolha a frequência de atualização:")
        print("1. 📊 A cada 6 horas (recomendado)")
        print("2. 🔄 A cada 12 horas")
        print("3. 📅 Uma vez por dia")
        print("4. 🗓️ Personalizado")
        
        opcao = input("\nEscolha uma opção (1-4): ").strip()
        
        frequencias = {
            '1': '0 */6 * * *',    # A cada 6 horas
            '2': '0 */12 * * *',   # A cada 12 horas
            '3': '0 9 * * *',      # Todo dia às 9h
        }
        
        if opcao in frequencias:
            cron_expr = frequencias[opcao]
        elif opcao == '4':
            cron_expr = input("Digite a expressão cron: ").strip()
        else:
            cron_expr = '0 9 * * *'  # Padrão
        
        # Cria script de automação
        script_content = f"""#!/bin/bash
# TrendHunter - Automação Completa
# Executado automaticamente via crontab

cd {os.getcwd()}

echo "🚀 $(date): Iniciando TrendHunter"

# 1. Atualiza tendências
python3 trend_hunter_pro.py

# 2. Executa sistema de monetização
python3 sistema_monetizacao.py

echo "✅ $(date): Automação concluída"
"""
        
        with open('automacao_trendhunter.sh', 'w') as f:
            f.write(script_content)
        
        os.chmod('automacao_trendhunter.sh', 0o755)
        
        # Cria configuração do crontab
        crontab_content = f"""
# TrendHunter - Automação
{cron_expr} cd {os.getcwd()} && ./automacao_trendhunter.sh >> logs/trendhunter.log 2>&1
"""
        
        with open('crontab_trendhunter', 'w') as f:
            f.write(crontab_content.strip())
        
        print("✅ Automação configurada!")
        print(f"⏰ Frequência: {cron_expr}")

    def instalar_dependencias(self):
        """Instala dependências Python necessárias"""
        print("\n📦 INSTALANDO DEPENDÊNCIAS")
        print("-" * 30)
        
        dependencias = [
            'pytrends',
            'beautifulsoup4',
            'requests',
            'python-telegram-bot'
        ]
        
        for dep in dependencias:
            print(f"📥 Instalando {dep}...")
            os.system(f"pip3 install {dep}")
        
        print("✅ Dependências instaladas!")

    def criar_estrutura_pastas(self):
        """Cria estrutura de pastas necessária"""
        print("\n📁 CRIANDO ESTRUTURA DE PASTAS")
        print("-" * 35)
        
        pastas = ['logs', 'backups', 'relatorios', 'configs']
        
        for pasta in pastas:
            os.makedirs(pasta, exist_ok=True)
            print(f"📂 Pasta criada: {pasta}/")
        
        print("✅ Estrutura criada!")

    def testar_sistema(self):
        """Testa se tudo está funcionando"""
        print("\n🧪 TESTANDO SISTEMA")
        print("-" * 25)
        
        # Testa imports
        try:
            import pytrends
            print("✅ PyTrends funcionando")
        except ImportError:
            print("❌ PyTrends não instalado")
        
        try:
            import requests
            print("✅ Requests funcionando")
        except ImportError:
            print("❌ Requests não instalado")
        
        # Testa arquivos
        arquivos_necessarios = [
            'trend_hunter_pro.py',
            'sistema_monetizacao.py',
            'index.html'
        ]
        
        for arquivo in arquivos_necessarios:
            if os.path.exists(arquivo):
                print(f"✅ {arquivo} encontrado")
            else:
                print(f"❌ {arquivo} não encontrado")

    def resumo_configuracao(self):
        """Exibe resumo da configuração"""
        print("\n" + "=" * 50)
        print("🎯 RESUMO DA CONFIGURAÇÃO")
        print("=" * 50)
        
        print(f"📊 APIs configuradas: {len(self.apis_configuradas)}")
        for api in self.apis_configuradas:
            print(f"   ✅ {api}")
        
        if not self.apis_configuradas:
            print("   ⚠️ Nenhuma API configurada ainda")
        
        print("\n🚀 PRÓXIMOS PASSOS:")
        print("1. Configure as APIs pendentes")
        print("2. Execute: python3 sistema_monetizacao.py")
        print("3. Abra dashboard.html no navegador")
        print("4. Configure automação: crontab crontab_trendhunter")
        
        print("\n💡 DICAS:")
        print("• Use 'python3 trend_hunter_pro.py' para testar")
        print("• Monitore logs em logs/trendhunter.log")
        print("• Acesse dashboard.html para controle visual")

    def menu_principal(self):
        """Menu principal interativo"""
        while True:
            print("\n" + "=" * 50)
            print("🎮 MENU PRINCIPAL - TRENDHUNTER")
            print("=" * 50)
            
            print("1. 📧 Configurar Mailchimp")
            print("2. 📱 Configurar Telegram Bot")
            print("3. 💎 Configurar WhatsApp Business")
            print("4. 💰 Configurar Google AdSense")
            print("5. ⚙️ Configurar Automação")
            print("6. 📦 Instalar Dependências")
            print("7. 📁 Criar Estrutura de Pastas")
            print("8. 🧪 Testar Sistema")
            print("9. 📋 Ver Resumo")
            print("0. 🚪 Sair")
            
            opcao = input("\n➤ Escolha uma opção: ").strip()
            
            if opcao == '1':
                self.configurar_mailchimp()
            elif opcao == '2':
                self.configurar_telegram()
            elif opcao == '3':
                self.configurar_whatsapp()
            elif opcao == '4':
                self.configurar_google_adsense()
            elif opcao == '5':
                self.configurar_automacao()
            elif opcao == '6':
                self.instalar_dependencias()
            elif opcao == '7':
                self.criar_estrutura_pastas()
            elif opcao == '8':
                self.testar_sistema()
            elif opcao == '9':
                self.resumo_configuracao()
            elif opcao == '0':
                print("\n👋 Saindo... Boa sorte com seu TrendHunter!")
                break
            else:
                print("❌ Opção inválida!")

def main():
    configurador = ConfiguradorTrendHunter()
    configurador.banner()
    
    print("\n🎯 Este script vai configurar todo o sistema TrendHunter")
    print("💡 Configure pelo menos 1 API para começar a monetizar")
    
    if input("\n➤ Continuar? (s/n): ").lower().startswith('s'):
        configurador.menu_principal()
    else:
        print("👋 Até mais!")

if __name__ == "__main__":
    main()