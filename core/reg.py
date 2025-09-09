from .db import get_connection
import json
import requests
from datetime import datetime
import re

def register_submission(landpage, name, email, form_data=None, newsletter=False):
    conn = get_connection()
    cur = conn.cursor()
    
    # Anonimizar dados do formulário para armazenamento
    form_fields = {}
    if form_data:
        # Remover dados sensíveis antes de armazenar
        for key, value in form_data.items():
            if key not in ['name', 'email']:  # Não armazenar nome e email diretamente
                # Anonimizar valores (armazenar apenas tipo e comprimento)
                form_fields[key] = f"{type(value).__name__}_{len(str(value)) if value else 0}"
    
    cur.execute("""
        INSERT INTO interacoes (
            usuario_id, pagina, primeira_acao, formulario_enviado, 
            formulario_campos, newsletter_inscrito, termos_aceitos
        ) VALUES (%s, %s, NOW(), %s, %s, %s, %s)
    """, (email, landpage, True, json.dumps(form_fields), newsletter, form_data.get('terms', False) if form_data else False))
    
    conn.commit()
    cur.close()
    conn.close()

def parse_user_agent(user_agent):
    """Parse user agent to extract device, browser, and OS information"""
    dispositivo = 'desktop'
    navegador = 'Other'
    sistema_operacional = 'Other'
    tipo_conexao = 'unknown'
    
    # Detectar dispositivo
    if any(keyword in user_agent for keyword in ['Mobile', 'Android', 'iPhone', 'iPad']):
        dispositivo = 'mobile'
    elif 'Windows' in user_agent or 'Macintosh' in user_agent or 'Linux' in user_agent:
        dispositivo = 'desktop'
    else:
        dispositivo = 'other'
    
    # Detectar navegador
    if 'Chrome' in user_agent and 'Edg' in user_agent:
        navegador = 'Edge'
    elif 'Chrome' in user_agent:
        navegador = 'Chrome'
    elif 'Firefox' in user_agent:
        navegador = 'Firefox'
    elif 'Safari' in user_agent:
        navegador = 'Safari'
    elif 'Edge' in user_agent:
        navegador = 'Edge'
    else:
        navegador = 'Other'
    
    # Detectar sistema operacional
    if 'Windows' in user_agent:
        sistema_operacional = 'Windows'
    elif 'Macintosh' in user_agent or 'Mac OS' in user_agent:
        sistema_operacional = 'Mac OS'
    elif 'Linux' in user_agent:
        sistema_operacional = 'Linux'
    elif 'Android' in user_agent:
        sistema_operacional = 'Android'
    elif 'iPhone' in user_agent or 'iPad' in user_agent:
        sistema_operacional = 'iOS'
    else:
        sistema_operacional = 'Other'
    
    # Detectar tipo de conexão aproximada
    if 'Mobile' in user_agent:
        tipo_conexao = 'mobile'
    else:
        tipo_conexao = 'broadband'
    
    return dispositivo, navegador, sistema_operacional, tipo_conexao

def get_geolocation_info(ip):
    """Obter informações de geolocalização a partir do IP"""
    try:
        # Em produção, você usaria um serviço real de geolocalização
        # Este é apenas um exemplo usando um serviço gratuito (limitado)
        # response = requests.get(f"http://ip-api.com/json/{ip}")
        # if response.status_code == 200:
        #     data = response.json()
        #     return {
        #         'regiao': f"{data.get('city', '')}, {data.get('regionName', '')}",
        #         'pais': data.get('country', ''),
        #         'provedor': data.get('isp', ''),
        #         'latitude': data.get('lat', ''),
        #         'longitude': data.get('lon', '')
        #     }
        # Para este exemplo, vamos retornar dados simulados
        return {
            'regiao': 'São Paulo, BR',
            'pais': 'Brasil',
            'provedor': 'ISP Exemplo',
            'latitude': '-23.5505',
            'longitude': '-46.6333'
        }
    except:
        return None

def register_visit(landpage, ip, user_agent, referer=None, utm_params=None, screen_resolution=None):
    conn = get_connection()
    cur = conn.cursor()
    
    # Parse user agent for detailed information
    dispositivo, navegador, sistema_operacional, tipo_conexao = parse_user_agent(user_agent)
    
    # Obter informações de geolocalização
    geo_info = get_geolocation_info(ip)
    regiao = geo_info['regiao'] if geo_info else ''
    provedor_internet = geo_info['provedor'] if geo_info else ''
    
    # Extrair parâmetros UTM se disponíveis
    utm_source = utm_params.get('utm_source', '') if utm_params else ''
    utm_medium = utm_params.get('utm_medium', '') if utm_params else ''
    utm_campaign = utm_params.get('utm_campaign', '') if utm_params else ''
    utm_term = utm_params.get('utm_term', '') if utm_params else ''
    utm_content = utm_params.get('utm_content', '') if utm_params else ''
    
    cur.execute("""
        INSERT INTO interacoes (
            usuario_id, pagina, navegador, dispositivo, sistema_operacional,
            primeira_interacao, user_agent, ip_address, referer,
            utm_source, utm_medium, campanha, utm_term, utm_content,
            resolucao_tela, horario_visita, regiao, provedor_internet, tipo_conexao
        ) VALUES (%s, %s, %s, %s, %s, NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s, %s, %s)
        RETURNING id
    """, (
        ip, landpage, navegador, dispositivo, sistema_operacional,
        user_agent, ip, referer,
        utm_source, utm_medium, utm_campaign, utm_term, utm_content,
        screen_resolution, regiao, provedor_internet, tipo_conexao
    ))
    
    visit_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return visit_id

def update_visit(visit_id, tempo_na_pagina, cliques, scroll_percent, origem, campanha, idioma, regiao, 
                 cliques_em_cta=0, tempo_ate_primeiro_clique=0, scroll_detalhado=None, 
                 tempo_em_secoes=None, eventos_personalizados=None, erros_javascript=None,
                 tempo_carregamento_pagina=None, provedor_internet=None, tipo_conexao=None):
    print(f"Updating visit {visit_id} with comprehensive data")
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        UPDATE interacoes 
        SET tempo_na_pagina = %s, 
            cliques = %s, 
            scroll_percent = %s, 
            origem = %s, 
            campanha = %s, 
            idioma = %s, 
            regiao = %s,
            cliques_em_cta = %s,
            tempo_ate_primeiro_clique = %s,
            scroll_detalhado = %s,
            tempo_em_secoes = %s,
            eventos_personalizados = %s,
            erros_javascript = %s,
            tempo_carregamento_pagina = %s,
            provedor_internet = %s,
            tipo_conexao = %s
        WHERE id = %s
    """, (
        tempo_na_pagina, cliques, scroll_percent, origem, campanha, idioma, regiao,
        cliques_em_cta, tempo_ate_primeiro_clique,
        json.dumps(scroll_detalhado) if scroll_detalhado else None,
        json.dumps(tempo_em_secoes) if tempo_em_secoes else None,
        json.dumps(eventos_personalizados) if eventos_personalizados else None,
        erros_javascript,
        tempo_carregamento_pagina,
        provedor_internet,
        tipo_conexao,
        visit_id
    ))
    
    conn.commit()
    cur.close()
    conn.close()
