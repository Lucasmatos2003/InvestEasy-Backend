# app/services.py

import requests
from datetime import datetime, timedelta
import os

# --- Variáveis de Cache Simples ---
# Em uma aplicação real, usaríamos um sistema de cache mais robusto como Redis ou Flask-Caching.
# Para este projeto, um dicionário em memória é suficiente para evitar chamadas repetidas.
cache = {}
CACHE_TIMEOUT_SECONDS = 3600 # 1 hora

def is_cache_valid(key):
    """Verifica se um item no cache ainda é válido."""
    if key not in cache:
        return False
    
    entry_time = cache[key]['timestamp']
    return (datetime.now() - entry_time).total_seconds() < CACHE_TIMEOUT_SECONDS

def get_indicadores_mercado():
    """
    Busca as taxas CDI e Selic mais recentes da API do Banco Central do Brasil.
    Implementa um sistema de cache simples e fallback.
    """
    cache_key = 'indicadores'
    
    if is_cache_valid(cache_key):
        return cache[cache_key]['data']

    try:
        # Busca a SELIC (código 11) e CDI (código 12) dos últimos 2 dias úteis
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11,12/dados/ultimos/2?formato=json"
        response = requests.get(url, timeout=5) # Timeout de 5 segundos
        response.raise_for_status() # Lança um erro para status HTTP 4xx/5xx
        dados = response.json()
        
        # Pega o valor mais recente de cada indicador
        selic_info = next((item for item in reversed(dados) if item['id_serie'] == 11), None)
        cdi_info = next((item for item in reversed(dados) if item['id_serie'] == 12), None)

        if not selic_info or not cdi_info:
            raise ValueError("Dados de SELIC ou CDI não encontrados na resposta da API")
            
        # Converte as taxas diárias para anuais (aproximação comum de mercado)
        taxa_selic_anual = ((1 + float(selic_info['valor']) / 100) ** 252) - 1
        taxa_cdi_anual = ((1 + float(cdi_info['valor']) / 100) ** 252) - 1

        resultado = {
            "selic": f"{taxa_selic_anual:.2%}",
            "cdi": f"{taxa_cdi_anual:.2%}",
            "selic_valor": taxa_selic_anual,
            "cdi_valor": taxa_cdi_anual,
            "data_referencia": datetime.strptime(selic_info['data'], '%d/%m/%Y').strftime('%Y-%m-%d')
        }
        
        # Armazena no cache
        cache[cache_key] = {'data': resultado, 'timestamp': datetime.now()}
        return resultado

    except (requests.RequestException, ValueError) as e:
        print(f"AVISO: Falha ao buscar dados do BCB: {e}. Verificando fallback no cache.")
        # Se a API falhar, usa o último dado válido no cache, mesmo que expirado
        if cache_key in cache:
            print("USANDO DADO ANTIGO DO CACHE (FALLBACK).")
            return cache[cache_key]['data']
        else:
            # Se não houver nada no cache, retorna um erro ou dados padrão
            return {"erro": "Não foi possível obter os dados de mercado."}


def calcular_aliquota_ir(dias):
    """
    Calcula a alíquota do Imposto de Renda com base na tabela regressiva.
    """
    if dias <= 180:
        return 0.225 # 22.5% [cite: 24]
    elif dias <= 360:
        return 0.20 # 20% [cite: 25]
    elif dias <= 720:
        return 0.175 # 17.5% [cite: 26]
    else:
        return 0.15 # 15% [cite: 26]

def simular_cdb(valor_inicial, prazo_dias, percentual_cdi):
    """
    Realiza a simulação de um investimento em CDB.
    """
    indicadores = get_indicadores_mercado()
    if "erro" in indicadores:
        return indicadores
    
    taxa_cdi_anual = indicadores['cdi_valor']
    
    # Converte o percentual do CDI para um fator (ex: 115% -> 1.15)
    fator_cdi = percentual_cdi / 100.0
    
    # Calcula a taxa de rendimento efetiva do CDB
    taxa_rendimento_anual = taxa_cdi_anual * fator_cdi
    
    # Converte a taxa anual para o período exato do investimento
    taxa_rendimento_periodo = (1 + taxa_rendimento_anual)**(prazo_dias / 365) - 1
    
    rendimento_bruto = valor_inicial * taxa_rendimento_periodo
    valor_bruto = valor_inicial + rendimento_bruto
    
    aliquota_ir = calcular_aliquota_ir(prazo_dias)
    valor_ir = rendimento_bruto * aliquota_ir
    
    valor_liquido = valor_bruto - valor_ir
    
    return {
        "tipo_investimento": f"CDB {percentual_cdi}% CDI",
        "dados_entrada": {
            "valor_investido": f"R$ {valor_inicial:,.2f}",
            "prazo_dias": prazo_dias,
            "taxa_utilizada": f"{percentual_cdi}% da CDI ({indicadores['cdi']})"
        },
        "resultados": {
            "rendimento_bruto": f"R$ {rendimento_bruto:,.2f}",
            "aliquota_ir": f"{aliquota_ir:.1%}",
            "valor_ir": f"R$ {valor_ir:,.2f}",
            "valor_liquido_final": f"R$ {valor_liquido:,.2f}"
        }
    }