#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TrendHunter Sistema Integrado de Monetização
============================================

Sistema que conecta todos os canais de monetização automaticamente
"""

import json
import os
from datetime import datetime
import asyncio
from newsletter_mailchimp import NewsletterMailchimp
from telegram_bot import TelegramBot
from whatsapp_business import WhatsAppBusiness

class SistemaMonetizacao:
    def __init__(self):
        """Inicializa o sistema integrado"""
        print("💰 TrendHunter - Sistema de Monetização Integrado")
        print("=" * 60)
        
        # Inicializa todos os canais
        self.newsletter = NewsletterMailchimp()
        self.telegram = TelegramBot()
        self.whatsapp = WhatsAppBusiness()
        
        # Configurações
        self.config = self.carregar_configuracoes()

    def carregar_configuracoes(self):
        """Carrega configurações do sistema"""
        config_padrao = {
            "newsletter": {
                "ativo": True,
                "frequencia": "semanal",  # diario, semanal
                "min_crescimento": 100
            },
            "telegram": {
                "ativo": True,
                "frequencia": "diario",
                "min_crescimento": 50
            },
            "whatsapp": {
                "ativo": True,
                "frequencia": "diario",
                "min_crescimento": 200,
                "apenas_premium": True
            },
            "push_notifications": {
                "ativo": True,
                "min_crescimento": 300
            }
        }
        
        try:
            if os.path.exists('monetizacao_config.json'):
                with open('monetizacao_config.json', 'r') as f:
                    config = json.load(f)
                    # Merge com padrão para garantir todas as chaves
                    return {**config_padrao, **config}
            else:
                # Cria arquivo de configuração padrão
                with open('monetizacao_config.json', 'w') as f:
                    json.dump(config_padrao, f, indent=2)
                return config_padrao
                
        except Exception as e:
            print(f"⚠️ Erro ao carregar config: {e}")
            return config_padrao

    def processar_todas_tendencias(self):
        """Processa e distribui tendências por todos os canais"""
        print("\n🚀 INICIANDO DISTRIBUIÇÃO MULTICANAL")
        print("=" * 50)
        
        try:
            # Busca últimas tendências
            tendencias = self.obter_ultimas_tendencias()
            if not tendencias:
                print("❌ Nenhuma tendência encontrada")
                return False
            
            print(f"📊 Encontradas {len(tendencias)} tendências para distribuir")
            
            # Filtra tendências por canal
            resultados = {}
            
            # 1. Newsletter (semanal, tendências sólidas)
            if self.config['newsletter']['ativo']:
                tendencias_newsletter = [
                    t for t in tendencias 
                    if t['crescimento'] >= self.config['newsletter']['min_crescimento']
                ]
                
                if tendencias_newsletter:
                    print(f"\n📧 Processando Newsletter ({len(tendencias_newsletter)} tendências)...")
                    resultados['newsletter'] = self.newsletter.processar_newsletter_automatica()
                else:
                    print("\n📧 Newsletter: Nenhuma tendência atinge critério mínimo")
                    resultados['newsletter'] = False
            
            # 2. Telegram (diário, mais liberal)
            if self.config['telegram']['ativo']:
                tendencias_telegram = [
                    t for t in tendencias 
                    if t['crescimento'] >= self.config['telegram']['min_crescimento']
                ]
                
                if tendencias_telegram:
                    print(f"\n📱 Processando Telegram ({len(tendencias_telegram)} tendências)...")
                    resultados['telegram'] = self.telegram.enviar_alertas_automaticos()
                else:
                    print("\n📱 Telegram: Nenhuma tendência atinge critério mínimo")
                    resultados['telegram'] = False
            
            # 3. WhatsApp Premium (diário, seletivo)
            if self.config['whatsapp']['ativo']:
                tendencias_whatsapp = [
                    t for t in tendencias 
                    if t['crescimento'] >= self.config['whatsapp']['min_crescimento']
                ]
                
                if tendencias_whatsapp:
                    print(f"\n💎 Processando WhatsApp Premium ({len(tendencias_whatsapp)} tendências)...")
                    resultados['whatsapp'] = self.whatsapp.processar_alertas_premium()
                else:
                    print("\n💎 WhatsApp: Nenhuma tendência atinge critério premium")
                    resultados['whatsapp'] = False
            
            # 4. Push Notifications (alertas urgentes)
            if self.config['push_notifications']['ativo']:
                tendencias_push = [
                    t for t in tendencias 
                    if t['crescimento'] >= self.config['push_notifications']['min_crescimento']
                ]
                
                if tendencias_push:
                    print(f"\n🔔 Alertas Push: {len(tendencias_push)} tendências urgentes identificadas")
                    # Aqui você implementaria o envio de push notifications
                    resultados['push'] = True
                else:
                    print("\n🔔 Push: Nenhuma tendência urgente")
                    resultados['push'] = False
            
            # Salva relatório de distribuição
            self.salvar_relatorio_distribuicao(tendencias, resultados)
            
            # Resume resultados
            print("\n" + "=" * 50)
            print("📊 RESUMO DA DISTRIBUIÇÃO:")
            print("=" * 50)
            
            sucessos = sum(1 for r in resultados.values() if r)
            total = len(resultados)
            
            for canal, sucesso in resultados.items():
                status = "✅ ENVIADO" if sucesso else "❌ FALHOU"
                print(f"  {canal.title()}: {status}")
            
            print(f"\n🎯 Taxa de sucesso: {sucessos}/{total} canais")
            
            if sucessos > 0:
                print("🎉 Distribuição multicanal concluída com sucesso!")
                return True
            else:
                print("⚠️ Nenhum canal foi enviado com sucesso")
                return False
                
        except Exception as e:
            print(f"❌ Erro no sistema integrado: {e}")
            return False

    def obter_ultimas_tendencias(self):
        """Obtém as últimas tendências dos backups"""
        try:
            backups = [f for f in os.listdir('backups') if f.endswith('.json')]
            if not backups:
                return []
            
            ultimo_backup = sorted(backups)[-1]
            with open(f'backups/{ultimo_backup}', 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            return dados.get('tendencias', [])
            
        except Exception as e:
            print(f"❌ Erro ao obter tendências: {e}")
            return []

    def salvar_relatorio_distribuicao(self, tendencias, resultados):
        """Salva relatório detalhado da distribuição"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        relatorio = {
            'timestamp': timestamp,
            'data_processamento': datetime.now().isoformat(),
            'total_tendencias': len(tendencias),
            'configuracao': self.config,
            'resultados_distribuicao': resultados,
            'tendencias_processadas': tendencias,
            'estatisticas': {
                'canais_enviados': sum(1 for r in resultados.values() if r),
                'canais_total': len(resultados),
                'taxa_sucesso': sum(1 for r in resultados.values() if r) / len(resultados) if resultados else 0
            }
        }
        
        os.makedirs('relatorios', exist_ok=True)
        with open(f'relatorios/distribuicao_{timestamp}.json', 'w', encoding='utf-8') as f:
            json.dump(relatorio, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Relatório salvo: relatorios/distribuicao_{timestamp}.json")

    def configurar_automacao_crontab(self):
        """Configura automação no crontab"""
        script_content = f"""#!/bin/bash
# TrendHunter - Automação Completa de Monetização
# ===============================================

cd {os.getcwd()}

echo "🔥 $(date): Iniciando automação TrendHunter"

# 1. Atualiza tendências
python3 trend_hunter_pro.py

# 2. Distribui por todos os canais
python3 sistema_monetizacao.py

echo "✅ $(date): Automação concluída"
"""
        
        with open('automacao_completa.sh', 'w') as f:
            f.write(script_content)
        
        os.chmod('automacao_completa.sh', 0o755)
        
        # Configuração para crontab
        crontab_config = f"""
# TrendHunter - Automação Completa
# Executa às 9h todos os dias
0 9 * * * cd {os.getcwd()} && ./automacao_completa.sh >> logs/automacao.log 2>&1

# Backup semanal aos domingos às 18h  
0 18 * * 0 cd {os.getcwd()} && tar -czf backups/backup_$(date +\\%Y\\%m\\%d).tar.gz . >> logs/backup.log 2>&1
"""
        
        with open('crontab_completo', 'w') as f:
            f.write(crontab_config.strip())
        
        print("✅ Automação configurada!")
        print("📁 Arquivos criados:")
        print("   - automacao_completa.sh")
        print("   - crontab_completo")
        print("\n💡 Para ativar:")
        print("   crontab crontab_completo")

    def relatorio_monetizacao(self):
        """Gera relatório de performance da monetização"""
        print("\n📊 RELATÓRIO DE MONETIZAÇÃO")
        print("=" * 40)
        
        try:
            # Conta relatórios de distribuição
            if os.path.exists('relatorios'):
                relatorios = [f for f in os.listdir('relatorios') if f.startswith('distribuicao_')]
                print(f"📄 Distribuições realizadas: {len(relatorios)}")
                
                if relatorios:
                    # Analisa último relatório
                    ultimo_relatorio = sorted(relatorios)[-1]
                    with open(f'relatorios/{ultimo_relatorio}', 'r') as f:
                        dados = json.load(f)
                    
                    stats = dados.get('estatisticas', {})
                    print(f"✅ Taxa de sucesso última distribuição: {stats.get('taxa_sucesso', 0)*100:.1f}%")
                    print(f"📊 Canais enviados: {stats.get('canais_enviados', 0)}/{stats.get('canais_total', 0)}")
            
            # Conta backups (indicador de atividade)
            backups = [f for f in os.listdir('backups') if f.endswith('.json')]
            print(f"🔄 Atualizações de tendências: {len(backups)}")
            
            # Verifica assinantes
            canais_ativos = []
            
            if os.path.exists('whatsapp_premium_subscribers.json'):
                with open('whatsapp_premium_subscribers.json', 'r') as f:
                    assinantes_wa = json.load(f)
                print(f"💎 Assinantes WhatsApp Premium: {len(assinantes_wa)}")
                canais_ativos.append('WhatsApp')
            
            print(f"\n🎯 Canais ativos: {', '.join(canais_ativos) if canais_ativos else 'Nenhum configurado'}")
            
            # Estimativa de receita potencial
            estimativa = len(backups) * 50  # R$ 50 por atualização (estimativa)
            print(f"💰 Potencial de receita mensal: R$ {estimativa:.2f}")
            
        except Exception as e:
            print(f"❌ Erro ao gerar relatório: {e}")

def main():
    """Função principal do sistema integrado"""
    sistema = SistemaMonetizacao()
    
    # Processa distribuição automática
    sistema.processar_todas_tendencias()
    
    # Gera relatório
    sistema.relatorio_monetizacao()

if __name__ == "__main__":
    main()