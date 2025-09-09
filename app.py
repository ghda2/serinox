from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import random
import os
import json
from urllib.parse import urlparse, parse_qs
from core.db import get_connection
from core.reg import register_submission, register_visit, update_visit

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    landpages = [d for d in os.listdir("templates") if os.path.isdir(os.path.join("templates", d)) and d.startswith("landpage")]
    landpage = random.choice(landpages)
    ip = request.client.host
    user_agent = request.headers.get('user-agent', '')
    referer = request.headers.get('referer', '')
    
    # Extrair parâmetros UTM da URL
    parsed_url = urlparse(str(request.url))
    query_params = parse_qs(parsed_url.query)
    utm_params = {
        'utm_source': query_params.get('utm_source', [None])[0],
        'utm_medium': query_params.get('utm_medium', [None])[0],
        'utm_campaign': query_params.get('utm_campaign', [None])[0],
        'utm_term': query_params.get('utm_term', [None])[0],
        'utm_content': query_params.get('utm_content', [None])[0],
    }
    
    # Obter resolução da tela do cabeçalho (se disponível)
    screen_resolution = request.headers.get('screen-resolution', '')
    
    visit_id = register_visit(landpage, ip, user_agent, referer, utm_params, screen_resolution)
    return templates.TemplateResponse(f"{landpage}/index.html", {
        "request": request, 
        "landpage": landpage, 
        "visit_id": visit_id
    })

@app.post("/submit")
async def submit(request: Request, name: str = Form(...), email: str = Form(...), landpage: str = Form(...)):
    # Coletar todos os dados do formulário
    form_data = await request.form()
    form_dict = dict(form_data)
    
    # Verificar se o usuário se inscreveu na newsletter
    newsletter = form_dict.get('newsletter', False)
    
    register_submission(landpage, name, email, form_dict, newsletter)
    return {"message": "Submission received"}

@app.post("/update_visit")
async def update_visit_endpoint(
    visit_id: int = Form(...),
    tempo_na_pagina: int = Form(...),
    cliques: int = Form(...),
    scroll_percent: int = Form(...),
    origem: str = Form(...),
    campanha: str = Form(...),
    idioma: str = Form(...),
    regiao: str = Form(...),
    cliques_em_cta: int = Form(0),
    tempo_ate_primeiro_clique: int = Form(0),
    scroll_detalhado: str = Form(None),
    tempo_em_secoes: str = Form(None),
    eventos_personalizados: str = Form(None),
    erros_javascript: str = Form(None),
    tempo_carregamento_pagina: int = Form(None),
    provedor_internet: str = Form(None),
    tipo_conexao: str = Form(None)
):
    # Converter strings JSON para objetos Python
    scroll_detalhado_obj = json.loads(scroll_detalhado) if scroll_detalhado else None
    tempo_em_secoes_obj = json.loads(tempo_em_secoes) if tempo_em_secoes else None
    eventos_personalizados_obj = json.loads(eventos_personalizados) if eventos_personalizados else None
    
    update_visit(
        visit_id, 
        tempo_na_pagina, 
        cliques, 
        scroll_percent, 
        origem, 
        campanha, 
        idioma, 
        regiao,
        cliques_em_cta,
        tempo_ate_primeiro_clique,
        scroll_detalhado_obj,
        tempo_em_secoes_obj,
        eventos_personalizados_obj,
        erros_javascript,
        tempo_carregamento_pagina,
        provedor_internet,
        tipo_conexao
    )
    return {"message": "Visit updated"}

@app.post("/newsletter")
async def newsletter(request: Request):
    form_data = await request.form()
    email = form_data.get('newsletter_email')
    if email:
        # Registrar inscrição na newsletter
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO interacoes (usuario_id, pagina, primeira_acao, newsletter_inscrito) 
            VALUES (%s, %s, NOW(), %s)
        """, (email, 'newsletter', True))
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Inscrição na newsletter realizada com sucesso"}
    return {"message": "Email não fornecido"}
