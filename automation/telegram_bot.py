#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TrendHunter Telegram Bot - Alertas Automáticos
==============================================

Bot do Telegram para enviar alertas de tendências automaticamente
"""

import json
import os
import requests
import asyncio
from datetime import datetime
import hashlib

class TelegramBot:
    def __init__(self):
        """Inicializa bot do Telegram"""
        print("📱 Inicializando Telegram Bot...")
        
        # Carrega configuração (produção ou local)
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.channel_id = os.getenv('TELEGRAM_CHANNEL_ID')
        
        if not self.bot_token or not self.channel_id:
            # Tenta carregar do arquivo local
            try:
                with open('config_telegram.json', 'r') as f:
                    config = json.load(f)
                    self.bot_token = config['bot_token']
                    self.channel_id = config['channel_id']
            except FileNotFoundError:
                print("❌ Configuração Telegram não encontrada!")
                print("💡 Configure via secrets GitHub ou execute: python3 configurador.py")
                self.bot_token = None
                self.channel_id = None
                return

    def enviar_mensagem(self, chat_id, texto, parse_mode='HTML'):
        """Envia mensagem para um chat específico"""
        url = f"{self.base_url}/sendMessage"
        
        data = {
            'chat_id': chat_id,
            'text': texto,
            'parse_mode': parse_mode,
            'disable_web_page_preview': False
        }
        
        try:
            response = requests.post(url, data=data)
            
            if response.status_code == 200:
                print(f"✅ Mensagem enviada para {chat_id}")
                return True
            else:
                print(f"❌ Erro ao enviar para {chat_id}: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Erro de conexão: {e}")
            return False

    def gerar_mensagem_tendencias(self, tendencias):
        """Gera mensagem formatada com as tendências"""
        data_hoje = datetime.now().strftime("%d/%m/%Y")
        hora_atual = datetime.now().strftime("%H:%M")
        
        # Emojis por categoria
        emojis = {
            'Tecnologia': '🤖',
            'E-commerce': '🛒', 
            'Finanças': '💰',
            'Saúde': '🏥',
            'Casa': '🏠'
        }
        
        mensagem = f"""🔥 <b>TENDÊNCIAS EXPLOSIVAS - {data_hoje}</b>
        
📊 <i>Atualizado às {hora_atual} | TrendHunter</i>

"""
        
        for i, tendencia in enumerate(tendencias[:5], 1):
            emoji = emojis.get(tendencia['categoria'], '📈')
            
            mensagem += f"""<b>{i}. {emoji} {tendencia['termo']}</b>
💹 <b>+{int(tendencia['crescimento'])}%</b> | 🏷️ {tendencia['categoria']}

{tendencia.get('descricao', 'Tendência emergente com alto potencial.')[:150]}...

"""
        
        mensagem += f"""
🚀 <b>Quer mais tendências exclusivas?</b>
👉 <a href="https://trendhunter.vercel.app">Acesse nosso site</a>

🔔 Para receber alertas automáticos:
👉 @trendhunter_br

#TrendHunter #Tendências #Negócios #Oportunidades"""
        
        return mensagem

    def gerar_mensagem_rapida(self, tendencia):
        """Gera alerta rápido para uma tendência específica"""
        emoji = {'Tecnologia': '🤖', 'E-commerce': '🛒', 'Finanças': '💰', 'Saúde': '🏥', 'Casa': '🏠'}.get(tendencia['categoria'], '📈')
        
        mensagem = f"""🚨 <b>ALERTA DE TENDÊNCIA!</b>

{emoji} <b>{tendencia['termo']}</b>
💹 <b>+{int(tendencia['crescimento'])}%</b> de crescimento!

{tendencia.get('descricao', 'Oportunidade emergente no mercado brasileiro.')[:200]}

🔥 Tendência identificada agora às {datetime.now().strftime('%H:%M')}

👉 <a href="https://trendhunter.vercel.app">Ver mais no TrendHunter</a>

#Alert #TrendHunter #{tendencia['categoria']}"""
        
        return mensagem

    def enviar_alertas_automaticos(self):
        """Envia alertas automáticos baseados nas últimas tendências"""
        print("📱 Processando alertas automáticos do Telegram...")
        
        try:
            # Busca últimas tendências
            backups = [f for f in os.listdir('backups') if f.endswith('.json')]
            if not backups:
                print("❌ Nenhum backup de tendências encontrado")
                return False
            
            ultimo_backup = sorted(backups)[-1]
            with open(f'backups/{ultimo_backup}', 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            tendencias = dados.get('tendencias', [])
            if not tendencias:
                print("❌ Nenhuma tendência encontrada")
                return False
            
            # Verifica se já enviou esse conjunto de tendências
            hash_tendencias = hashlib.md5(str(tendencias).encode()).hexdigest()
            arquivo_hash = 'telegram_last_sent.txt'
            
            if os.path.exists(arquivo_hash):
                with open(arquivo_hash, 'r') as f:
                    ultimo_hash = f.read().strip()
                
                if hash_tendencias == ultimo_hash:
                    print("⚠️ Tendências já enviadas anteriormente")
                    return True
            
            # Gera e envia mensagem
            mensagem = self.gerar_mensagem_tendencias(tendencias)
            
            # Envia para canal público
            sucesso = self.enviar_mensagem(self.channel_id, mensagem)
            
            if sucesso:
                # Salva hash para evitar duplicatas
                with open(arquivo_hash, 'w') as f:
                    f.write(hash_tendencias)
                
                print("🎉 Alertas enviados com sucesso!")
                return True
            else:
                return False
                
        except Exception as e:
            print(f"❌ Erro ao processar alertas: {e}")
            return False

    def enviar_alerta_tendencia_alta(self, limite_crescimento=300):
        """Envia alerta especial para tendências com crescimento muito alto"""
        try:
            backups = [f for f in os.listdir('backups') if f.endswith('.json')]
            if not backups:
                return False
            
            ultimo_backup = sorted(backups)[-1]
            with open(f'backups/{ultimo_backup}', 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            tendencias = dados.get('tendencias', [])
            
            # Filtra tendências com crescimento muito alto
            tendencias_alta = [t for t in tendencias if t['crescimento'] >= limite_crescimento]
            
            for tendencia in tendencias_alta:
                mensagem = self.gerar_mensagem_rapida(tendencia)
                self.enviar_mensagem(self.channel_id, mensagem)
                
            if tendencias_alta:
                print(f"🚨 Enviados {len(tendencias_alta)} alertas de crescimento alto!")
                return True
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False

    def configurar_webhook(self, webhook_url):
        """Configura webhook para receber atualizações"""
        url = f"{self.base_url}/setWebhook"
        
        data = {
            'url': webhook_url
        }
        
        try:
            response = requests.post(url, data=data)
            
            if response.status_code == 200:
                print(f"✅ Webhook configurado: {webhook_url}")
                return True
            else:
                print(f"❌ Erro ao configurar webhook: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False

    def obter_info_bot(self):
        """Obtém informações sobre o bot"""
        url = f"{self.base_url}/getMe"
        
        try:
            response = requests.get(url)
            
            if response.status_code == 200:
                info = response.json()
                print(f"🤖 Bot: @{info['result']['username']}")
                print(f"📝 Nome: {info['result']['first_name']}")
                return info['result']
            else:
                print(f"❌ Erro ao obter info: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            return None

def criar_script_automatico():
    """Cria script para execução automática do bot"""
    script_content = """#!/usr/bin/env python3
# Script automático para alertas Telegram

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram_bot import TelegramBot

# Inicializa bot
bot = TelegramBot()

# Envia alertas automáticos
bot.enviar_alertas_automaticos()

# Envia alertas de crescimento alto (opcional)
bot.enviar_alerta_tendencia_alta(250)
"""
    
    with open('telegram_auto.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    os.chmod('telegram_auto.py', 0o755)
    print("✅ Script automático criado: telegram_auto.py")

if __name__ == "__main__":
    # Exemplo de uso
    bot = TelegramBot()
    
    print("\n📱 CONFIGURAÇÃO DO BOT TELEGRAM:")
    print("1. Crie um bot com @BotFather no Telegram")
    print("2. Crie um canal público (ex: @trendhunter_br)")
    print("3. Adicione o bot como admin do canal")
    print("4. Configure as variáveis de ambiente:")
    print("   export TELEGRAM_BOT_TOKEN='seu_bot_token'")
    print("   export TELEGRAM_CHANNEL_ID='@seu_canal'")
    print("\n5. Para enviar alertas automáticos:")
    print("   bot.enviar_alertas_automaticos()")
    print("\n6. Para criar script automático:")
    criar_script_automatico()