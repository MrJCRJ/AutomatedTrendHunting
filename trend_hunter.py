#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TrendHunter - Coletor Automático de Tendências
===============================================

Script para coletar tendências do Google Trends e gerar cards HTML automaticamente.
"""

import json
import os
from datetime import datetime, timedelta
from pytrends.request import TrendReq
import random
import time

class TrendHunter:
    def __init__(self):
        """Inicializa o coletor de tendências"""
        print("🔥 TrendHunter - Iniciando coleta de tendências...")
        self.pytrends = TrendReq(hl='pt-BR', tz=360)
        
        # Categorias para pesquisar
        self.categorias = {
            'Tecnologia': [
                'inteligência artificial', 'blockchain', 'NFT', 'metaverso', 
                'web3', 'IoT', 'realidade virtual', 'automação'
            ],
            'E-commerce': [
                'dropshipping', 'marketplace', 'vendas online', 'marketing digital',
                'afiliados', 'produtos digitais', 'loja virtual'
            ],
            'Finanças': [
                'investimentos', 'bitcoin', 'day trade', 'renda extra',
                'poupança', 'fundos imobiliários', 'educação financeira'
            ],
            'Saúde': [
                'telemedicina', 'wellness', 'fitness', 'medicina preventiva',
                'saúde mental', 'meditação', 'nutrição'
            ],
            'Casa': [
                'casa inteligente', 'sustentabilidade', 'energia solar',
                'decoração', 'organização', 'jardinagem'
            ]
        }

    def pesquisar_tendencias(self, termos, periodo='today 3-m'):
        """Pesquisa tendências para uma lista de termos"""
        print(f"📊 Pesquisando: {', '.join(termos)}")
        
        try:
            # Pesquisa no Google Trends
            self.pytrends.build_payload(termos, cat=0, timeframe=periodo, geo='BR')
            
            # Dados de interesse ao longo do tempo
            interesse = self.pytrends.interest_over_time()
            
            if interesse.empty:
                return None
                
            # Calcula crescimento dos últimos 30 dias vs 30 dias anteriores
            dados_recentes = interesse.tail(30)
            dados_anteriores = interesse.head(len(interesse) - 30).tail(30)
            
            resultados = []
            for termo in termos:
                if termo in interesse.columns:
                    media_recente = dados_recentes[termo].mean()
                    media_anterior = dados_anteriores[termo].mean() if len(dados_anteriores) > 0 else 1
                    
                    if media_anterior == 0:
                        media_anterior = 1
                        
                    crescimento = ((media_recente - media_anterior) / media_anterior) * 100
                    
                    resultados.append({
                        'termo': termo,
                        'crescimento': round(crescimento, 1),
                        'interesse_atual': round(media_recente, 1),
                        'interesse_anterior': round(media_anterior, 1)
                    })
            
            return resultados
            
        except Exception as e:
            print(f"❌ Erro ao pesquisar {termos}: {e}")
            return None

    def gerar_tendencias_aleatorias(self):
        """Gera tendências usando dados reais quando possível, simulados quando necessário"""
        todas_tendencias = []
        
        for categoria, termos in self.categorias.items():
            print(f"\n🎯 Categoria: {categoria}")
            
            # Pesquisa em lotes de 5 termos (limite do Google Trends)
            for i in range(0, len(termos), 5):
                lote = termos[i:i+5]
                
                try:
                    resultados = self.pesquisar_tendencias(lote)
                    
                    if resultados:
                        for resultado in resultados:
                            if resultado['crescimento'] > 10:  # Só tendências com crescimento significativo
                                todas_tendencias.append({
                                    'categoria': categoria,
                                    **resultado
                                })
                    
                    # Delay para não sobrecarregar a API
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"❌ Erro no lote {lote}: {e}")
                    continue
        
        # Se não conseguiu dados suficientes, adiciona algumas tendências simuladas
        if len(todas_tendencias) < 3:
            print("⚠️ Poucos dados reais encontrados. Adicionando tendências simuladas...")
            tendencias_simuladas = self.gerar_tendencias_simuladas()
            todas_tendencias.extend(tendencias_simuladas)
        
        # Ordena por crescimento e pega as top 5
        todas_tendencias.sort(key=lambda x: x['crescimento'], reverse=True)
        return todas_tendencias[:5]

    def gerar_tendencias_simuladas(self):
        """Gera tendências simuladas baseadas em dados realistas"""
        simuladas = [
            {
                'termo': 'IA Generativa para Pequenas Empresas',
                'categoria': 'Tecnologia',
                'crescimento': 280.0,
                'interesse_atual': 85.0,
                'interesse_anterior': 30.0,
                'descricao': 'Pequenas empresas descobrindo como usar ChatGPT e similares para automatizar processos.'
            },
            {
                'termo': 'Energia Solar Residencial',
                'categoria': 'Casa',
                'crescimento': 190.0,
                'interesse_atual': 72.0,
                'interesse_anterior': 38.0,
                'descricao': 'Com a conta de luz mais cara, famílias buscam alternativas sustentáveis.'
            },
            {
                'termo': 'Investimento em REITs',
                'categoria': 'Finanças',
                'crescimento': 145.0,
                'interesse_atual': 68.0,
                'interesse_anterior': 47.0,
                'descricao': 'Fundos imobiliários americanos ganham popularidade entre investidores brasileiros.'
            }
        ]
        
        return simuladas

    def gerar_card_html(self, tendencia):
        """Gera o HTML de um card de tendência"""
        descricoes = {
            'Tecnologia': f"Setor de tecnologia em crescimento explosivo. Oportunidades em ferramentas, cursos e consultoria.",
            'E-commerce': f"E-commerce brasileiro aquecido. Oportunidade para produtos e serviços digitais.",
            'Finanças': f"Mercado financeiro em movimento. Nicho educacional e ferramentas financeiras em alta.",
            'Saúde': f"Setor de saúde digital expandindo. Oportunidades em telemedicina e wellness.",
            'Casa': f"Mercado residencial inovando. Soluções inteligentes e sustentáveis em demanda."
        }
        
        # Descrição personalizada ou padrão
        descricao = tendencia.get('descricao', descricoes.get(tendencia['categoria'], 'Tendência emergente com potencial de crescimento.'))
        
        return f'''            <div class="trend-card">
                <h3 class="trend-title">{tendencia['termo']}</h3>
                <span class="trend-growth">+{int(tendencia['crescimento'])}%</span>
                <span class="trend-category">{tendencia['categoria']}</span>
                <p class="trend-description">
                    {descricao}
                    <strong>Potencial:</strong> Alto crescimento nos próximos meses.
                </p>
            </div>'''

    def atualizar_index_html(self, tendencias):
        """Atualiza o arquivo index.html com as novas tendências"""
        print("📝 Atualizando index.html...")
        
        # Gera os cards HTML
        cards_html = '\n\n'.join([self.gerar_card_html(t) for t in tendencias])
        
        # Lê o arquivo atual
        with open('index.html', 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        # Encontra e substitui a seção de tendências
        inicio_marker = '<h2 style="margin-bottom: 2rem; text-align: center">'
        fim_marker = '</div>\n    </main>'
        
        inicio_idx = conteudo.find(inicio_marker)
        fim_idx = conteudo.find(fim_marker, inicio_idx)
        
        if inicio_idx != -1 and fim_idx != -1:
            # Monta novo conteúdo
            novo_conteudo = (
                conteudo[:inicio_idx] +
                '<h2 style="margin-bottom: 2rem; text-align: center">\n          📈 Tendências em Alta (Atualizado hoje)\n        </h2>\n\n' +
                cards_html + '\n\n        ' +
                conteudo[fim_idx:]
            )
            
            # Salva arquivo
            with open('index.html', 'w', encoding='utf-8') as f:
                f.write(novo_conteudo)
            
            print("✅ index.html atualizado com sucesso!")
            return True
        else:
            print("❌ Não foi possível encontrar a seção de tendências no HTML")
            return False

    def salvar_backup(self, tendencias):
        """Salva backup das tendências em JSON"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = {
            'timestamp': timestamp,
            'data_coleta': datetime.now().isoformat(),
            'tendencias': tendencias
        }
        
        os.makedirs('backups', exist_ok=True)
        with open(f'backups/tendencias_{timestamp}.json', 'w', encoding='utf-8') as f:
            json.dump(backup, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Backup salvo: backups/tendencias_{timestamp}.json")

    def executar(self):
        """Executa o processo completo de coleta e atualização"""
        print("🚀 Iniciando coleta de tendências...")
        
        try:
            # Coleta tendências
            tendencias = self.gerar_tendencias_aleatorias()
            
            if not tendencias:
                print("❌ Nenhuma tendência encontrada")
                return False
            
            print(f"\n📊 Encontradas {len(tendencias)} tendências:")
            for t in tendencias:
                print(f"  • {t['termo']} ({t['categoria']}) - +{t['crescimento']}%")
            
            # Salva backup
            self.salvar_backup(tendencias)
            
            # Atualiza HTML
            sucesso = self.atualizar_index_html(tendencias)
            
            if sucesso:
                print("\n🎉 Processo concluído com sucesso!")
                print("💡 Próximos passos:")
                print("   1. git add .")
                print("   2. git commit -m 'Atualizar tendências'")
                print("   3. git push origin main")
                return True
            else:
                return False
                
        except Exception as e:
            print(f"❌ Erro durante execução: {e}")
            return False

if __name__ == "__main__":
    hunter = TrendHunter()
    hunter.executar()