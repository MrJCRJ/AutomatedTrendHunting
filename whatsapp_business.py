#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TrendHunter WhatsApp Business - Alertas Premium
==============================================

Sistema de WhatsApp Business para envio de alertas premium
"""

import json
import os
import requests
from datetime import datetime
import hashlib

class WhatsAppBusiness:
    def __init__(self):
        """Inicializa o sistema WhatsApp Business"""
        self.access_token = os.getenv('WHATSAPP_ACCESS_TOKEN', 'YOUR_ACCESS_TOKEN_HERE')
        self.phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID', 'YOUR_PHONE_NUMBER_ID')
        self.business_account_id = os.getenv('WHATSAPP_BUSINESS_ACCOUNT_ID', 'YOUR_BUSINESS_ACCOUNT_ID')
        self.base_url = "https://graph.facebook.com/v18.0"
        
        print("📱 WhatsApp Business - Inicializando...")

    def enviar_mensagem_texto(self, numero_destino, mensagem):
        """Envia mensagem de texto simples"""
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "messaging_product": "whatsapp",
            "to": numero_destino,
            "type": "text",
            "text": {
                "body": mensagem
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                print(f"✅ Mensagem enviada para {numero_destino}")
                return True
            else:
                print(f"❌ Erro ao enviar: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Erro de conexão: {e}")
            return False

    def enviar_template_tendencias(self, numero_destino, tendencias):
        """Envia template estruturado com tendências"""
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        # Monta lista de tendências para template
        components = [
            {
                "type": "header",
                "parameters": [
                    {
                        "type": "text",
                        "text": f"🔥 {len(tendencias)} Tendências Explosivas"
                    }
                ]
            },
            {
                "type": "body",
                "parameters": [
                    {
                        "type": "text", 
                        "text": datetime.now().strftime("%d/%m/%Y")
                    }
                ]
            }
        ]
        
        data = {
            "messaging_product": "whatsapp",
            "to": numero_destino,
            "type": "template",
            "template": {
                "name": "tendencias_premium",  # Nome do template aprovado
                "language": {
                    "code": "pt_BR"
                },
                "components": components
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                print(f"✅ Template enviado para {numero_destino}")
                return True
            else:
                print(f"❌ Erro ao enviar template: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False

    def gerar_mensagem_premium(self, tendencias):
        """Gera mensagem premium formatada"""
        data_hoje = datetime.now().strftime("%d/%m/%Y")
        hora_atual = datetime.now().strftime("%H:%M")
        
        mensagem = f"""🔥 *TRENDHUNTER PREMIUM* 🔥

📅 {data_hoje} às {hora_atual}
💎 Alertas Exclusivos para Assinantes

"""
        
        for i, tendencia in enumerate(tendencias[:3], 1):  # Top 3 para WhatsApp
            emoji = {'Tecnologia': '🤖', 'E-commerce': '🛒', 'Finanças': '💰', 'Saúde': '🏥', 'Casa': '🏠'}.get(tendencia['categoria'], '📈')
            
            mensagem += f"""*{i}. {emoji} {tendencia['termo']}*
💹 +{int(tendencia['crescimento'])}% | 🏷️ {tendencia['categoria']}

{tendencia.get('descricao', 'Oportunidade emergente.')[:100]}...

💡 *Potencial de mercado:* Alto
⚡ *Urgência:* Imediata

"""
        
        mensagem += f"""
🎯 *ANÁLISE EXCLUSIVA PREMIUM:*

• Estas tendências foram identificadas com nossa IA avançada
• Dados cruzados de Google Trends + Reddit + Análise de Sentimento  
• Recomendação: Ação imediata para aproveitamento máximo

💰 *OPORTUNIDADES DE MONETIZAÇÃO:*
• Criação de produtos/serviços
• Marketing de afiliados
• Desenvolvimento de cursos
• Consultoria especializada

🔗 *Acesse análise completa:*
https://trendhunter.vercel.app

📞 *Suporte Premium:* Responda esta mensagem
🚫 *Para cancelar:* Digite STOP

---
© TrendHunter Premium 2025"""
        
        return mensagem

    def enviar_alerta_urgente(self, numero_destino, tendencia):
        """Envia alerta urgente para tendência de alto crescimento"""
        emoji = {'Tecnologia': '🤖', 'E-commerce': '🛒', 'Finanças': '💰', 'Saúde': '🏥', 'Casa': '🏠'}.get(tendencia['categoria'], '📈')
        
        mensagem = f"""🚨 *ALERTA URGENTE* 🚨

{emoji} *{tendencia['termo']}*

📊 *CRESCIMENTO: +{int(tendencia['crescimento'])}%*
🕒 *Identificado agora às {datetime.now().strftime('%H:%M')}*

{tendencia.get('descricao', 'Oportunidade crítica identificada.')[:150]}

⚡ *AÇÃO RECOMENDADA:*
• Análise imediata de viabilidade
• Pesquisa de concorrência
• Desenvolvimento de estratégia de entrada

🔗 *Ver detalhes:*
https://trendhunter.vercel.app

💎 *TrendHunter Premium*"""
        
        return self.enviar_mensagem_texto(numero_destino, mensagem)

    def processar_alertas_premium(self):
        """Processa e envia alertas para assinantes premium"""
        print("📱 Processando alertas premium WhatsApp...")
        
        try:
            # Carrega lista de assinantes premium
            if not os.path.exists('whatsapp_premium_subscribers.json'):
                print("⚠️ Nenhum assinante premium encontrado")
                return False
            
            with open('whatsapp_premium_subscribers.json', 'r') as f:
                assinantes = json.load(f)
            
            if not assinantes:
                print("⚠️ Lista de assinantes vazia")
                return False
            
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
            
            # Verifica se já enviou para evitar spam
            hash_tendencias = hashlib.md5(str(tendencias).encode()).hexdigest()
            arquivo_hash = 'whatsapp_last_sent.txt'
            
            if os.path.exists(arquivo_hash):
                with open(arquivo_hash, 'r') as f:
                    ultimo_hash = f.read().strip()
                
                if hash_tendencias == ultimo_hash:
                    print("⚠️ Tendências já enviadas anteriormente")
                    return True
            
            # Gera mensagem premium
            mensagem = self.gerar_mensagem_premium(tendencias)
            
            # Envia para todos os assinantes
            sucessos = 0
            for assinante in assinantes:
                numero = assinante.get('numero')
                nome = assinante.get('nome', 'Assinante')
                
                if numero:
                    sucesso = self.enviar_mensagem_texto(numero, mensagem)
                    if sucesso:
                        sucessos += 1
                        print(f"✅ Enviado para {nome} ({numero})")
                    else:
                        print(f"❌ Falha para {nome} ({numero})")
            
            if sucessos > 0:
                # Salva hash para evitar duplicatas
                with open(arquivo_hash, 'w') as f:
                    f.write(hash_tendencias)
                
                print(f"🎉 Alertas enviados para {sucessos}/{len(assinantes)} assinantes!")
                return True
            else:
                print("❌ Nenhum alerta enviado com sucesso")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao processar alertas: {e}")
            return False

    def adicionar_assinante_premium(self, numero, nome, plano="premium"):
        """Adiciona novo assinante premium"""
        try:
            # Carrega lista existente
            if os.path.exists('whatsapp_premium_subscribers.json'):
                with open('whatsapp_premium_subscribers.json', 'r') as f:
                    assinantes = json.load(f)
            else:
                assinantes = []
            
            # Verifica se já existe
            for assinante in assinantes:
                if assinante['numero'] == numero:
                    print(f"⚠️ {numero} já é assinante premium")
                    return True
            
            # Adiciona novo assinante
            novo_assinante = {
                'numero': numero,
                'nome': nome,
                'plano': plano,
                'data_inscricao': datetime.now().isoformat(),
                'ativo': True
            }
            
            assinantes.append(novo_assinante)
            
            # Salva lista atualizada
            with open('whatsapp_premium_subscribers.json', 'w') as f:
                json.dump(assinantes, f, indent=2, ensure_ascii=False)
            
            print(f"✅ {nome} ({numero}) adicionado como assinante premium")
            
            # Envia mensagem de boas-vindas
            mensagem_boas_vindas = f"""🎉 *Bem-vindo ao TrendHunter Premium!* 🎉

Olá *{nome}*! 👋

Você agora faz parte do nosso grupo seleto de assinantes premium e receberá:

🔥 *Alertas exclusivos* das tendências mais quentes
📊 *Análises avançadas* com potencial de mercado
⚡ *Alertas urgentes* para oportunidades críticas
💎 *Insights premium* não disponíveis no site gratuito

Seus primeiros alertas chegam em breve!

💰 *Transforme tendências em negócios lucrativos*

🔗 Site: https://trendhunter.vercel.app
📞 Suporte: Responda esta mensagem"""
            
            self.enviar_mensagem_texto(numero, mensagem_boas_vindas)
            return True
            
        except Exception as e:
            print(f"❌ Erro ao adicionar assinante: {e}")
            return False

    def configurar_webhook(self, webhook_url, verify_token):
        """Configura webhook para receber mensagens"""
        print(f"🔗 Configure o webhook no Facebook Developers:")
        print(f"   URL: {webhook_url}")
        print(f"   Verify Token: {verify_token}")
        print(f"   Subscription Fields: messages")

def criar_lista_exemplo():
    """Cria lista de exemplo com assinantes premium"""
    assinantes_exemplo = [
        {
            "numero": "5511999999999",  # Formato: código do país + DDD + número
            "nome": "João Silva",
            "plano": "premium",
            "data_inscricao": datetime.now().isoformat(),
            "ativo": True
        }
    ]
    
    with open('whatsapp_premium_subscribers.json', 'w') as f:
        json.dump(assinantes_exemplo, f, indent=2, ensure_ascii=False)
    
    print("✅ Lista de exemplo criada: whatsapp_premium_subscribers.json")

if __name__ == "__main__":
    # Exemplo de uso
    whatsapp = WhatsAppBusiness()
    
    print("\n📱 CONFIGURAÇÃO WHATSAPP BUSINESS:")
    print("1. Cadastre-se no WhatsApp Business Platform")
    print("2. Configure o número de telefone")
    print("3. Obtenha as credenciais de API")
    print("4. Configure as variáveis de ambiente:")
    print("   export WHATSAPP_ACCESS_TOKEN='seu_token'")
    print("   export WHATSAPP_PHONE_NUMBER_ID='seu_phone_id'")
    print("   export WHATSAPP_BUSINESS_ACCOUNT_ID='seu_account_id'")
    print("\n5. Para criar lista de assinantes de exemplo:")
    criar_lista_exemplo()
    print("\n6. Para processar alertas premium:")
    print("   whatsapp.processar_alertas_premium()")