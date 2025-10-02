#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TrendHunter Newsletter - Sistema de Envio Automático
===================================================

Integração com Mailchimp para envios automáticos de newsletter
"""

import json
import os
from datetime import datetime, timedelta
import requests
import hashlib

class NewsletterMailchimp:
    def __init__(self):
        """Inicializa cliente Mailchimp"""
        print("📧 Inicializando Newsletter Mailchimp...")
        
        # Carrega configuração (produção ou local)
        self.api_key = os.getenv('MAILCHIMP_API_KEY')
        self.audience_id = os.getenv('MAILCHIMP_AUDIENCE_ID')
        
        if not self.api_key or not self.audience_id:
            # Tenta carregar do arquivo local
            try:
                with open('config_mailchimp.json', 'r') as f:
                    config = json.load(f)
                    self.api_key = config['api_key']
                    self.audience_id = config['audience_id']
            except FileNotFoundError:
                print("❌ Configuração Mailchimp não encontrada!")
                print("� Configure via secrets GitHub ou execute: python3 configurador.py")
                self.api_key = None
                self.audience_id = None
                return

    def adicionar_contato(self, email, nome="", fonte="site"):
        """Adiciona contato à lista do Mailchimp"""
        url = f"{self.base_url}/lists/{self.audience_id}/members"
        
        data = {
            "email_address": email,
            "status": "subscribed",
            "merge_fields": {
                "FNAME": nome,
                "SOURCE": fonte,
                "SIGNUP": datetime.now().strftime("%Y-%m-%d")
            },
            "tags": ["trendhunter", "auto-signup"]
        }
        
        headers = {
            "Authorization": f"Bearer {self.mailchimp_api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                print(f"✅ Email {email} adicionado com sucesso!")
                return True
            elif response.status_code == 400:
                # Provavelmente já existe
                print(f"⚠️ Email {email} já existe na lista")
                return True
            else:
                print(f"❌ Erro ao adicionar {email}: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Erro de conexão: {e}")
            return False

    def criar_campanha_newsletter(self, tendencias, assunto=None):
        """Cria uma campanha de newsletter com as tendências"""
        if not assunto:
            data_hoje = datetime.now().strftime("%d/%m/%Y")
            assunto = f"🔥 5 Tendências Explosivas - {data_hoje} | TrendHunter"
        
        # Gera HTML da newsletter
        html_newsletter = self.gerar_html_newsletter(tendencias, assunto)
        
        # Cria campanha
        url = f"{self.base_url}/campaigns"
        
        data = {
            "type": "regular",
            "recipients": {
                "list_id": self.audience_id
            },
            "settings": {
                "subject_line": assunto,
                "title": f"TrendHunter Newsletter - {datetime.now().strftime('%Y-%m-%d')}",
                "from_name": "TrendHunter",
                "reply_to": "contato@trendhunter.com",
                "preview_text": "Descubra as tendências que estão explodindo antes de todo mundo! 🚀"
            }
        }
        
        headers = {
            "Authorization": f"Bearer {self.mailchimp_api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                campanha = response.json()
                campanha_id = campanha['id']
                print(f"✅ Campanha criada: {campanha_id}")
                
                # Adiciona conteúdo HTML
                sucesso_html = self.definir_conteudo_campanha(campanha_id, html_newsletter)
                
                if sucesso_html:
                    return campanha_id
                else:
                    return None
            else:
                print(f"❌ Erro ao criar campanha: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Erro de conexão: {e}")
            return None

    def definir_conteudo_campanha(self, campanha_id, html_conteudo):
        """Define o conteúdo HTML da campanha"""
        url = f"{self.base_url}/campaigns/{campanha_id}/content"
        
        data = {
            "html": html_conteudo
        }
        
        headers = {
            "Authorization": f"Bearer {self.mailchimp_api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.put(url, json=data, headers=headers)
            
            if response.status_code == 200:
                print("✅ Conteúdo da campanha definido")
                return True
            else:
                print(f"❌ Erro ao definir conteúdo: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Erro de conexão: {e}")
            return False

    def enviar_campanha(self, campanha_id):
        """Envia a campanha para todos os assinantes"""
        url = f"{self.base_url}/campaigns/{campanha_id}/actions/send"
        
        headers = {
            "Authorization": f"Bearer {self.mailchimp_api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, headers=headers)
            
            if response.status_code == 204:
                print("🚀 Newsletter enviada com sucesso!")
                return True
            else:
                print(f"❌ Erro ao enviar: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Erro de conexão: {e}")
            return False

    def gerar_html_newsletter(self, tendencias, assunto):
        """Gera HTML completo da newsletter"""
        data_hoje = datetime.now().strftime("%d de %B de %Y")
        
        # Gera cards das tendências
        cards_html = ""
        for i, tendencia in enumerate(tendencias, 1):
            emoji = {'Tecnologia': '🤖', 'E-commerce': '🛒', 'Finanças': '💰', 'Saúde': '🏥', 'Casa': '🏠'}.get(tendencia['categoria'], '📈')
            
            cards_html += f"""
            <tr>
                <td style="padding: 20px; background: white; margin-bottom: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h3 style="color: #667eea; font-size: 18px; margin-bottom: 10px;">{emoji} {tendencia['termo']}</h3>
                    <div style="margin-bottom: 10px;">
                        <span style="background: #28a745; color: white; padding: 4px 8px; border-radius: 4px; font-size: 14px; margin-right: 8px;">+{int(tendencia['crescimento'])}%</span>
                        <span style="background: #6c757d; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">{tendencia['categoria']}</span>
                    </div>
                    <p style="color: #666; line-height: 1.5;">{tendencia.get('descricao', 'Tendência emergente com alto potencial de crescimento.')}</p>
                </td>
            </tr>
            <tr><td style="height: 15px;"></td></tr>
            """
        
        html = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{assunto}</title>
        </head>
        <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f8f9fa;">
            <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f8f9fa;">
                <tr>
                    <td align="center" style="padding: 40px 20px;">
                        <table width="600" cellpadding="0" cellspacing="0" style="background-color: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                            
                            <!-- Header -->
                            <tr>
                                <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center;">
                                    <h1 style="color: white; margin: 0; font-size: 28px;">🔥 TrendHunter</h1>
                                    <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 16px;">Tendências Exclusivas - {data_hoje}</p>
                                </td>
                            </tr>
                            
                            <!-- Intro -->
                            <tr>
                                <td style="padding: 30px;">
                                    <h2 style="color: #333; margin: 0 0 15px 0;">Olá, Caçador de Tendências! 👋</h2>
                                    <p style="color: #666; line-height: 1.6; margin: 0;">
                                        Aqui estão as <strong>5 tendências mais explosivas</strong> que identificamos esta semana. 
                                        Essas oportunidades podem ser o próximo grande negócio! 🚀
                                    </p>
                                </td>
                            </tr>
                            
                            <!-- Tendências -->
                            <tr>
                                <td style="padding: 0 30px;">
                                    <table width="100%" cellpadding="0" cellspacing="0">
                                        {cards_html}
                                    </table>
                                </td>
                            </tr>
                            
                            <!-- CTA -->
                            <tr>
                                <td style="padding: 30px; text-align: center; background: #f8f9fa;">
                                    <h3 style="color: #333; margin: 0 0 15px 0;">💡 Quer mais insights exclusivos?</h3>
                                    <p style="color: #666; margin: 0 0 20px 0;">Acesse nosso site para análises detalhadas e novas tendências diárias!</p>
                                    <a href="https://trendhunter.vercel.app" style="background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: bold;">📈 Ver Mais Tendências</a>
                                </td>
                            </tr>
                            
                            <!-- Footer -->
                            <tr>
                                <td style="padding: 20px; text-align: center; background: #333; color: white;">
                                    <p style="margin: 0; font-size: 14px;">
                                        © 2025 TrendHunter - Feito com ❤️ para empreendedores brasileiros
                                    </p>
                                    <p style="margin: 10px 0 0 0; font-size: 12px; color: #ccc;">
                                        <a href="*|UNSUB|*" style="color: #ccc;">Cancelar inscrição</a> | 
                                        <a href="*|ARCHIVE|*" style="color: #ccc;">Ver no navegador</a>
                                    </p>
                                </td>
                            </tr>
                            
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
        
        return html

    def processar_newsletter_automatica(self):
        """Processa e envia newsletter automática com últimas tendências"""
        print("📧 Processando newsletter automática...")
        
        # Busca últimas tendências do backup mais recente
        try:
            backups = [f for f in os.listdir('backups') if f.endswith('.json')]
            if not backups:
                print("❌ Nenhum backup de tendências encontrado")
                return False
            
            ultimo_backup = sorted(backups)[-1]
            with open(f'backups/{ultimo_backup}', 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            tendencias = dados.get('tendencias', [])
            if not tendencias:
                print("❌ Nenhuma tendência encontrada no backup")
                return False
            
            print(f"📊 Encontradas {len(tendencias)} tendências para newsletter")
            
            # Cria e envia campanha
            campanha_id = self.criar_campanha_newsletter(tendencias[:5])  # Top 5
            
            if campanha_id:
                # Para teste, não envia automaticamente
                print(f"✅ Campanha criada: {campanha_id}")
                print("💡 Para enviar: newsletter.enviar_campanha('{campanha_id}')")
                
                # Salva ID da campanha para referência
                with open('newsletter_campaign.json', 'w') as f:
                    json.dump({
                        'campaign_id': campanha_id,
                        'created_at': datetime.now().isoformat(),
                        'trends_count': len(tendencias)
                    }, f)
                
                return True
            else:
                return False
                
        except Exception as e:
            print(f"❌ Erro ao processar newsletter: {e}")
            return False

if __name__ == "__main__":
    # Exemplo de uso
    newsletter = NewsletterMailchimp()
    
    print("\n📧 CONFIGURAÇÃO DA NEWSLETTER:")
    print("1. Cadastre-se no Mailchimp (gratuito até 2000 contatos)")
    print("2. Crie uma audiência/lista")
    print("3. Configure as variáveis de ambiente:")
    print("   export MAILCHIMP_API_KEY='sua_api_key'")
    print("   export MAILCHIMP_AUDIENCE_ID='seu_audience_id'")
    print("\n4. Para enviar newsletter automática:")
    print("   newsletter.processar_newsletter_automatica()")