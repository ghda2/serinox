DROP TABLE IF EXISTS submissions;
DROP TABLE IF EXISTS visits;

CREATE TABLE interacoes (
    id SERIAL PRIMARY KEY,
    usuario_id VARCHAR(100),          -- hash/cookie/sessão
    pagina VARCHAR(100),              -- qual página
    tempo_na_pagina INT,              -- em segundos
    cliques INT,                      -- nº de cliques
    scroll_percent SMALLINT,          -- % rolada
    origem VARCHAR(100),              -- ex: google, insta
    campanha VARCHAR(100),            -- utm_campaign
    idioma VARCHAR(10),               -- ex: pt-BR
    regiao VARCHAR(100),              -- ex: São Paulo, BR
    dispositivo VARCHAR(50),          -- mobile, desktop
    navegador VARCHAR(50),            -- Chrome, Safari, etc.
    primeira_interacao TIMESTAMP,     -- quando entrou
    primeira_acao TIMESTAMP,          -- quando clicou pela 1ª vez
    retorno BOOLEAN DEFAULT FALSE,    -- já visitou antes?
    criado_em TIMESTAMP DEFAULT NOW(),
    -- Novos campos para melhor tracking
    utm_source VARCHAR(100),          -- parâmetro utm_source
    utm_medium VARCHAR(100),          -- parâmetro utm_medium
    utm_term VARCHAR(100),            -- parâmetro utm_term
    utm_content VARCHAR(100),         -- parâmetro utm_content
    referer VARCHAR(500),             -- página de referência
    resolucao_tela VARCHAR(50),       -- resolução da tela do usuário
    sistema_operacional VARCHAR(50),  -- sistema operacional
    user_agent TEXT,                  -- user agent completo
    horario_visita TIMESTAMP,         -- horário exato da visita
    tempo_ate_primeiro_clique INT,    -- tempo até o primeiro clique (em segundos)
    cliques_em_cta INT DEFAULT 0,     -- cliques em elementos de call-to-action
    tempo_em_secoes JSON,             -- tempo gasto em diferentes seções da página
    eventos_personalizados JSON,      -- eventos personalizados disparados
    formulario_enviado BOOLEAN DEFAULT FALSE,  -- se o formulário foi enviado
    formulario_campos JSON,           -- dados dos campos do formulário (anonimizados)
    newsletter_inscrito BOOLEAN DEFAULT FALSE, -- se o usuário se inscreveu na newsletter
    termos_aceitos BOOLEAN DEFAULT FALSE,      -- se os termos foram aceitos
    scroll_detalhado JSON,            -- tracking detalhado de scroll (pontos específicos)
    ip_address VARCHAR(45),           -- endereço IP do usuário
    provedor_internet VARCHAR(100),   -- provedor de internet (se possível identificar)
    tipo_conexao VARCHAR(50),         -- tipo de conexão (móvel, wifi, etc.)
    tempo_carregamento_pagina INT,    -- tempo de carregamento da página (em ms)
    erros_javascript TEXT             -- erros de JavaScript ocorridos
);
