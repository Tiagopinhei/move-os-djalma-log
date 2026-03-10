# ==============================================================================
# BLOCO 1: FUNDAÇÃO, FERRAMENTAS E DESIGN VISUAL (UI/UX)
# ==============================================================================
# Este bloco prepara o ambiente, importa as bibliotecas de engenharia e dados, 
# e define a identidade visual da Djalma Log usando CSS avançado.
# ==============================================================================

import streamlit as st
import math
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from fpdf import FPDF
import base64

# 1.1 CONFIGURAÇÃO DE ALTO NÍVEL DA PÁGINA
st.set_page_config(
    page_title="Djalma Log - Inteligência em Logística",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 1.2 INJEÇÃO DE CSS PERSONALIZADO (ENGINEERING DESIGN SYSTEM)
# Aqui estamos mudando a "lataria" do Streamlit para o Azul Djalma Log (#000033)
st.markdown("""
    <style>
    /* Importando fontes modernas */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    /* Reset Geral */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #f8fafd;
    }

    /* Estilização da Barra Lateral e Containers */
    .stApp {
        background-image: linear-gradient(180deg, #f0f4f8 0%, #ffffff 100%);
    }

    /* Cards de Inventário (Efeito de Profundidade) */
    div[data-testid="stExpander"] {
        background-color: white !important;
        border-radius: 12px !important;
        border: 1px solid #e0e6ed !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02) !important;
        margin-bottom: 15px !important;
        transition: 0.3s;
    }
    div[data-testid="stExpander"]:hover {
        border-color: #000033 !important;
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.05) !important;
    }

    /* Botão de Cálculo (Estilo High-Performance) */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #000033 0%, #000066 100%) !important;
        color: #ffffff !important;
        height: 4.5em !important;
        width: 100% !important;
        font-weight: 800 !important;
        font-size: 20px !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        border-radius: 15px !important;
        border: none !important;
        box-shadow: 0 10px 20px rgba(0, 0, 51, 0.2) !important;
        transition: all 0.4s ease !important;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 30px rgba(0, 0, 51, 0.3) !important;
        background: linear-gradient(90deg, #000066 0%, #000099 100%) !important;
    }

    /* Customização das Abas (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 60px !important;
        background-color: #ffffff !important;
        border-radius: 12px 12px 0px 0px !important;
        border: 1px solid #e0e6ed !important;
        padding: 0px 30px !important;
        font-weight: 600 !important;
        color: #666 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #000033 !important;
        color: #ffffff !important;
        border: 1px solid #000033 !important;
    }

    /* Métricas e Dashboard */
    [data-testid="stMetric"] {
        background-color: #ffffff !important;
        padding: 20px !important;
        border-radius: 15px !important;
        border-left: 5px solid #000033 !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.03) !important;
    }
    [data-testid="stMetricValue"] {
        color: #000033 !important;
        font-weight: 800 !important;
    }

    /* Ajuste de Inputs */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 1.3 CABEÇALHO E BRANDING DO SISTEMA
# Criando um Header limpo e profissional
col_logo, col_info = st.columns([1, 4])

with col_info:
    st.title("MoveOS 6.0: Gestão Logística")
    st.markdown("""
        **Djalma Log Fretes e Mudanças** *Engenharia de Transporte, Cubagem Automática e Orçamentação Digital.*
    """)

# Banner de Status do Sistema
st.info("🔄 Sistema Online: Motor de GPS e Cálculo de Cubagem Ativos.")

# 1.4 BARRA LATERAL DE CONFIGURAÇÕES (ADMIN)
with st.sidebar:
    st.header("⚙️ Painel do Gestor")
    st.write("Configurações de Margem e Custos")
    taxa_combustivel = st.slider("Custo do Diesel (R$/km)", 1.0, 10.0, 3.5)
    taxa_ajudante = st.number_input("Diária Ajudante (R$)", value=100.0)
    taxa_minima_global = st.number_input("Taxa Mínima Local (R$)", value=350.0)
    st.divider()
    st.caption("v6.0.2 - Desenvolvido para Djalma Log")

# Espaçamento de segurança
st.markdown("<br>", unsafe_allow_html=True)
# ==============================================================================
# BLOCO 2: O CÉREBRO - DADOS, LOGÍSTICA E DOCUMENTAÇÃO (PDF)
# ==============================================================================
# Este bloco contém as funções matemáticas, o banco de dados de móveis e a 
# lógica de geração do documento oficial de orçamento.
# ==============================================================================

# 2.1 BANCO DE DADOS TÉCNICO DE CUBAGEM (m³)
# Valores baseados em padrões de transporte logístico residencial e comercial.
CATALOGO_TECNICO = {
    "Sala e Escritório": {
        "Sofá 2 Lugares": 1.00, "Sofá 3 Lugares": 1.50, "Poltrona": 0.50,
        "Estante/Rack": 0.80, "Mesa de Centro": 0.30, "Mesa de Jantar (6 lug)": 1.50,
        "Cadeira": 0.20, "Aparador": 0.45, "Escrivaninha": 0.70, "Cadeira de Escritório": 0.35,
        "Piano Vertical": 2.50, "Ar Condicionado (Split)": 0.40
    },
    "Quartos": {
        "Cama Casal (Box/Padrão)": 1.50, "Cama Solteiro": 0.80, "Beliche": 1.20,
        "Guarda-Roupa 2 Portas": 1.20, "Guarda-Roupa 4 Portas": 2.50, "Cômoda": 0.70,
        "Criado-Mudo": 0.15, "Penteadeira": 0.60, "Berço": 0.50, "Sapateira": 0.40
    },
    "Cozinha e Área": {
        "Geladeira Simples": 1.00, "Geladeira Side-by-Side": 1.80, "Freezer": 1.20,
        "Fogão 4 Bocas": 0.50, "Fogão 6 Bocas": 0.70, "Micro-ondas": 0.20,
        "Máquina de Lavar": 0.80, "Máquina de Secar": 0.70, "Lava-Louças": 0.60,
        "Armário de Cozinha (Módulo)": 0.50, "Bujão de Gás": 0.15
    },
    "Diversos e Frágeis": {
        "Televisor (LCD/LED)": 0.30, "Computador/Monitor": 0.25, "Espelho Grande": 0.20,
        "Tampo de Vidro": 0.35, "Bicicleta": 0.50, "Ventilador": 0.10,
        "Caixa de Papelão Média": 0.25, "Caixa de Papelão Grande": 0.45, "Mala de Viagem": 0.30,
        "Vaso de Planta": 0.20, "Tapete Grande": 0.20
    }
}

# 2.2 MOTOR DE GPS E CÁLCULO DE DISTÂNCIA
# Utiliza a API do Nominatim (OpenStreetMap) e Geodésica para precisão em km.
def obter_logistica_rota(origem, destino):
    geolocator = Nominatim(user_agent="moveos_djalmalog_v6")
    try:
        loc1 = geolocator.geocode(origem + ", Brasil", timeout=10)
        loc2 = geolocator.geocode(destino + ", Brasil", timeout=10)
        
        if loc1 and loc2:
            coord1 = (loc1.latitude, loc1.longitude)
            coord2 = (loc2.latitude, loc2.longitude)
            # Cálculo da distância em linha reta com fator de correção de 25% para estradas
            distancia_real = geodesic(coord1, coord2).kilometers * 1.25
            return round(distancia_real, 2)
        return None
    except Exception as e:
        return None

# 2.3 GERADOR DE DOCUMENTO OFICIAL (PDF)
# Cria um PDF profissional com a identidade da Djalma Log.
def exportar_pdf_final(dados):
    pdf = FPDF()
    pdf.add_page()
    
    # Configuração de Cores e Estilo
    pdf.set_fill_color(0, 0, 51) # Azul Djalma Log
    pdf.rect(0, 0, 210, 40, 'F') # Faixa de Cabeçalho
    
    # Título do Cabeçalho
    pdf.set_font("Arial", 'B', 22)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(190, 20, txt="DJALMA LOG - PROPOSTA COMERCIAL", ln=True, align='C')
    
    pdf.set_font("Arial", '', 10)
    pdf.cell(190, 5, txt="Inteligência em Transportes e Logística Residencial", ln=True, align='C')
    pdf.ln(20)
    
    # Dados do Cliente e Rota
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(100, 10, txt="INFORMAÇÕES GERAIS", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(100, 7, txt=f"Data da Proposta: {datetime.now().strftime('%d/%m/%Y')}", ln=True)
    pdf.cell(100, 7, txt=f"Data da Mudança: {dados['data_mudanca']}", ln=True)
    pdf.cell(100, 7, txt=f"Origem: {dados['origem']}", ln=True)
    pdf.cell(100, 7, txt=f"Destino: {dados['destino']}", ln=True)
    pdf.ln(5)
    
    # Detalhamento da Carga (A lógica matemática aqui é essencial)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(100, 10, txt="ESPECIFICAÇÕES TÉCNICAS DA MUDANÇA", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(100, 7, txt=f"- Volume Total Estimado: {dados['volume']:.2f} m3", ln=True)
    pdf.cell(100, 7, txt=f"- Capacidade do Veículo: {dados['capacidade_veiculo']} m3", ln=True)
    pdf.cell(100, 7, txt=f"- Número de Viagens Necessárias: {dados['viagens']}", ln=True)
    pdf.cell(100, 7, txt=f"- Equipe Escalada: {dados['ajudantes']} ajudantes", ln=True)
    pdf.ln(5)

    # Tabela de Preços e Serviços
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(100, 10, txt="RESUMO FINANCEIRO", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(100, 7, txt=f"Serviço de Transporte (Frete): R$ {dados['preco_frete']:.2f}", ln=True)
    pdf.cell(100, 7, txt=f"Mão de Obra e Ajudantes: R$ {dados['preco_equipe']:.2f}", ln=True)
    
    if dados['adicionais']:
        pdf.cell(100, 7, txt=f"Taxas Adicionais (Embalagem/Escadas): R$ {dados['taxas_extras']:.2f}", ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 100, 0)
    pdf.cell(190, 12, txt=f"VALOR TOTAL DO INVESTIMENTO: R$ {dados['total_geral']:.2f}", border=1, ln=True, align='C')
    
    # Rodapé Legal
    pdf.ln(20)
    pdf.set_font("Arial", 'I', 8)
    pdf.set_text_color(150, 150, 150)
    msg_legal = "Este orçamento tem validade de 10 dias. O valor final pode sofrer alterações caso o inventário real divirja do informado neste documento."
    pdf.multi_cell(190, 5, txt=msg_legal, align='C')
    
    return pdf.output(dest='S').encode('latin-1')

# 2.4 LÓGICA DE CÁLCULO DE CUBAGEM (Engenharia de Carga)
# O volume total é calculado pela somatória: $$V_{total} = \sum_{i=1}^{n} (Qtd_i \cdot Vol_i)$$
def calcular_metricas_logistica(inventario, dist, min_local, valor_km, valor_ajudante, taxas_extras):
    volume_total = sum(item['qtd'] * item['m3'] for item in inventario)
    
    # Capacidade padrão do caminhão VW Baú da Djalma Log (Exemplo: 40m3)
    CAPACIDADE_CAMINHAO = 40.0
    viagens = math.ceil(volume_total / CAPACIDADE_CAMINHAO)
    if viagens == 0: viagens = 1
    
    # Equipe sugerida: 1 ajudante a cada 12m3 de carga, mínimo 2
    ajudantes = max(2, math.ceil(volume_total / 12.0))
    
    # Cálculo Financeiro
    if dist <= 50:
        # Frete Urbano/Local
        preco_frete = min_local * viagens
    else:
        # Frete Interestadual/Longa Distância (Ida + Volta cobrada)
        # Arredondamos a distância para blocos de 50km para margem de segurança
        distancia_faturada = math.ceil(dist / 50.0) * 50
        preco_frete = (distancia_faturada * 2) * viagens * valor_km
    
    preco_equipe = ajudantes * valor_ajudante
    total_geral = preco_frete + preco_equipe + taxas_extras
    
    return {
        "volume": volume_total,
        "viagens": viagens,
        "ajudantes": ajudantes,
        "preco_frete": preco_frete,
        "preco_equipe": preco_equipe,
        "total_geral": total_geral,
        "capacidade_veiculo": CAPACIDADE_CAMINHAO
    }
    # ==============================================================================
# BLOCO 3: INTERFACE DE COMANDO, ROTAS E INVENTÁRIO DINÂMICO
# ==============================================================================
# Este bloco constrói a experiência do usuário, organizando a coleta de dados
# em abas e expanders para garantir que nenhum item seja esquecido.
# ==============================================================================

# 3.1 ORGANIZAÇÃO POR ABAS (FLUXO DE TRABALHO)
# Separamos o processo em 3 etapas para não sobrecarregar o usuário.
tab_logistica, tab_inventario, tab_servicos = st.tabs([
    "📍 1. Rota e Logística", 
    "📦 2. Inventário de Carga", 
    "🛠️ 3. Serviços e Adicionais"
])

# 3.2 ABA 1: LOGÍSTICA DE DESLOCAMENTO
with tab_logistica:
    st.subheader("Configurações de Trajeto")
    st.markdown("Informe os pontos de coleta e entrega para cálculo de quilometragem real.")
    
    col_rota1, col_rota2 = st.columns(2)
    with col_rota1:
        origem_input = st.text_input("Cidade de Origem", placeholder="Ex: Teresina, PI", help="Informe Cidade e Sigla do Estado.")
        data_mudanca = st.date_input("Data pretendida para a mudança", min_value=datetime.now())
    with col_rota2:
        destino_input = st.text_input("Cidade de Destino", placeholder="Ex: Parnaíba, PI")
        tipo_residencia = st.selectbox("Tipo de Mudança", ["Residencial (Casa)", "Residencial (Apartamento)", "Comercial/Escritório"])

    st.info("💡 **Dica da Djalma Log:** Verifique se as ruas permitem o acesso de caminhões de grande porte no dia escolhido.")

# 3.3 ABA 2: INVENTÁRIO DETALHADO (O "FECHA-BRECHAS")
# Aqui criamos um dicionário temporário para armazenar o que o usuário selecionar.
inventario_selecionado = []

with tab_inventario:
    st.subheader("Inventário Completo por Ambientes")
    st.write("Selecione a quantidade de itens que serão transportados em cada cômodo:")

    # Iteramos sobre o Catálogo Técnico criado no Bloco 2
    for ambiente, itens in CATALOGO_TECNICO.items():
        with st.expander(f"📂 {ambiente}", expanded=(ambiente == "Sala e Escritório")):
            # Criamos colunas para o inventário não ficar uma lista infinita
            cols_inv = st.columns(3)
            for i, (nome_item, m3_item) in enumerate(itens.items()):
                with cols_inv[i % 3]:
                    qtd = st.number_input(f"{nome_item}", min_value=0, max_value=50, step=1, key=f"inv_{nome_item}")
                    if qtd > 0:
                        inventario_selecionado.append({
                            "item": nome_item,
                            "qtd": qtd,
                            "m3": m3_item
                        })

    # Seção de Itens Extras (A "Aba Outros" que você pediu)
    st.markdown("---")
    st.write("✨ **Itens Não Listados / Observações de Carga**")
    col_ex1, col_ex2 = st.columns([3, 1])
    item_extra_nome = col_ex1.text_input("Descreva o item extra (Ex: Cofre, Aquário, Mesa de Sinuca...)")
    vol_extra_unitario = col_ex2.number_input("Volume Estimado (m³)", min_value=0.0, step=0.1, help="Pequeno: 0.2 | Médio: 1.0 | Grande: 2.0+")
    
    if item_extra_nome and vol_extra_unitario > 0:
        inventario_selecionado.append({
            "item": f"EXTRA: {item_extra_nome}",
            "qtd": 1,
            "m3": vol_extra_unitario
        })

# 3.4 ABA 3: SERVIÇOS ADICIONAIS E COMPLEXIDADE
with tab_servicos:
    st.subheader("Nível de Serviço e Dificuldades")
    st.write("Selecione os adicionais que exigem mais tempo ou materiais da equipe.")
    
    col_sv1, col_sv2 = st.columns(2)
    with col_sv1:
        servico_embalagem = st.toggle("📦 Preciso que a Djalma Log EMBALE meus pertences", help="Inclui plástico bolha, papelão e caixas.")
        servico_desmontagem = st.toggle("🔧 Preciso de DESMONTAGEM e MONTAGEM de móveis")
    with col_sv2:
        possui_escadas = st.toggle("🪜 O local possui ESCADAS (Sem elevador)", help="Sinalize se houver mais de um lance de escada.")
        item_fragil_extremo = st.toggle("💎 Possuo itens de altíssima fragilidade (Cristaleiras/Vidros)", help="Ativa protocolos de proteção extra.")

    st.markdown("---")
    obs_geral = st.text_area("Notas Adicionais para a Equipe (Ex: Horário de condomínio, local de difícil estacionamento...)")

# Espaçamento para o botão de ação que virá no próximo bloco
st.markdown("<br>", unsafe_allow_html=True)
# ==============================================================================
# BLOCO 4: O PROCESSADOR DE ORÇAMENTOS E DASHBOARD DE RESULTADOS
# ==============================================================================
# Este bloco executa a lógica de cálculo, valida os dados geográficos e
# apresenta o resultado final em um formato de painel de indicadores (KPIs).
# ==============================================================================

# 4.1 BOTÃO DE EXECUÇÃO (TRIGGER DO SISTEMA)
st.markdown("---")
if st.button("CALCULAR ORÇAMENTO FINAL E GERAR PROPOSTA"):
    
    # Validação de Entrada: Se não houver rota ou carga, o sistema trava.
    if not origem_input or not destino_input:
        st.error("⚠️ Erro de Logística: As cidades de ORIGEM e DESTINO são obrigatórias.")
    elif len(inventario_selecionado) == 0:
        st.error("⚠️ Erro de Carga: O inventário está vazio. Adicione itens para calcular a cubagem.")
    else:
        # Iniciamos o processamento visual
        with st.spinner("🚀 Consultando satélites GPS e dimensionando frota..."):
            
            # Chamada ao Motor de GPS (Bloco 2)
            distancia_km = obter_logistica_rota(origem_input, destino_input)
            
            if distancia_km is None:
                st.error("❌ Falha de Geolocalização: Não conseguimos encontrar as cidades informadas. Verifique a ortografia.")
            else:
                # 4.2 CÁLCULO DE TAXAS EXTRAS (REGRAS DE NEGÓCIO)
                # Aplicamos custos adicionais baseados nos toggles da Aba 3.
                taxas_extras_total = 0.0
                servicos_lista = []

                if servico_embalagem:
                    # R$ 35,00 por m3 embalado (cobre material e tempo)
                    taxas_extras_total += (sum(i['qtd'] * i['m3'] for i in inventario_selecionado) * 35.0)
                    servicos_lista.append("Embalagem Profissional")
                
                if servico_desmontagem:
                    # Taxa fixa de desmontagem técnica
                    taxas_extras_total += 250.0
                    servicos_lista.append("Desmontagem/Montagem")
                
                if possui_escadas:
                    # Adicional de insalubridade/esforço da equipe
                    taxas_extras_total += 180.0
                    servicos_lista.append("Adicional de Escadas")
                
                if item_fragil_extremo:
                    # Seguro e proteção extra para vidros/cristais
                    taxas_extras_total += 120.0
                    servicos_lista.append("Proteção para Frágeis")

                # 4.3 PROCESSAMENTO DAS MÉTRICAS FINAIS
                # Chamamos a função mestre de cálculo do Bloco 2
                resultados = calcular_metricas_logistica(
                    inventario_selecionado, 
                    distancia_km, 
                    taxa_minima_global, 
                    taxa_combustivel, 
                    taxa_ajudante, 
                    taxas_extras_total
                )

                # 4.4 DASHBOARD DE RESULTADOS (VISUALIZAÇÃO PREMIUM)
                st.success(f"✅ Orçamento Concluído para {data_mudanca.strftime('%d/%m/%Y')}!")
                
                # Primeira Linha: Indicadores de Operação
                col_met1, col_met2, col_met3, col_met4 = st.columns(4)
                col_met1.metric("Distância (Ida)", f"{distancia_km} km")
                col_met2.metric("Volume Total", f"{resultados['volume']:.2f} m³")
                col_met3.metric("Equipe", f"{resultados['ajudantes']} Ajudantes")
                col_met4.metric("Logística", f"{resultados['viagens']} Viagem(ns)")

                # Segunda Linha: Detalhamento Financeiro
                st.markdown("### 💰 Detalhamento Financeiro")
                col_fin1, col_fin2 = st.columns(2)
                
                with col_fin1:
                    st.write("**Custos Operacionais:**")
                    st.write(f"- Transporte e Combustível: R$ {resultados['preco_frete']:.2f}")
                    st.write(f"- Mão de Obra Especializada: R$ {resultados['preco_equipe']:.2f}")
                    if taxas_extras_total > 0:
                        st.write(f"- Serviços Adicionais: R$ {taxas_extras_total:.2f}")
                
                with col_fin2:
                    st.markdown(f"""
                        <div style="background-color:#000033; padding:20px; border-radius:15px; text-align:center;">
                            <h2 style="color:white; margin:0;">VALOR TOTAL</h2>
                            <h1 style="color:#00ff00; margin:0;">R$ {resultados['total_geral']:.2f}</h1>
                            <p style="color:white; font-size:12px;">*Sujeito a alteração após vistoria presencial</p>
                        </div>
                    """, unsafe_allow_html=True)

                # 4.5 PREPARAÇÃO DO PDF (DADOS PARA O BLOCO 5)
                # Guardamos os resultados em uma variável de sessão para o próximo bloco.
                st.session_state['dados_proposta'] = {
                    "origem": origem_input,
                    "destino": destino_input,
                    "data_mudanca": data_mudanca.strftime("%d/%m/%Y"),
                    "volume": resultados['volume'],
                    "capacidade_veiculo": resultados['capacidade_veiculo'],
                    "viagens": resultados['viagens'],
                    "ajudantes": resultados['ajudantes'],
                    "preco_frete": resultados['preco_frete'],
                    "preco_equipe": resultados['preco_equipe'],
                    "taxas_extras": taxas_extras_total,
                    "adicionais": servicos_lista,
                    "total_geral": resultados['total_geral']
                }
                
                st.balloons()
                # ==============================================================================
# ==============================================================================
# BLOCO 5: ÁREA DO GESTOR E CONTATO DIRETO
# ==============================================================================

# 5.1 LOGIN ADMINISTRATIVO (NA SIDEBAR)
with st.sidebar:
    st.divider()
    st.subheader("🔑 Área do Gestor")
    senha = st.text_input("Senha de Acesso", type="password")
    
    # Senha simples para você e seu pai (mude depois)
    acesso_admin = (senha == "djalma2026") 
    
    if acesso_admin:
        st.success("Acesso Liberado, Tiago!")
        st.write("Agora você pode editar a agenda no painel principal.")

# 5.2 SEÇÃO DE SUPORTE E AGENDA (PÓS-ORÇAMENTO)
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

col_footer1, col_footer2 = st.columns(2)

with col_footer1:
    st.subheader("📅 Agenda de Disponibilidade")
    
    # Se o admin estiver logado, ele pode editar as datas
    if acesso_admin:
        st.info("🛠️ Modo Edição Ativo")
        novas_datas = st.text_input("Atualizar Datas Ocupadas (separe por vírgula)", "12/03, 15/03, 18/03")
        if st.button("Salvar Alterações na Agenda"):
            st.session_state['agenda_txt'] = novas_datas
            st.success("Agenda atualizada!")
    
    # Exibição para o cliente
    agenda_atual = st.session_state.get('agenda_txt', "12/03, 15/03, 18/03")
    st.warning(f"🚫 **Datas Ocupadas nesta Quinzena:** {agenda_atual}")
    st.success("🟢 **Demais datas:** Disponibilidade para saída imediata com o VW Baú.")
    st.date_input("Consulte sua data no calendário:", min_value=datetime.now())

with col_footer2:
    st.subheader("📞 Fale com o Djalma")
    st.write("Dúvidas sobre o frete? Chame agora mesmo no canal oficial:")
    
    # WhatsApp Direto (Sem intermediário)
    link_wpp_direto = "https://wa.me/5586988629083?text=Olá%20Djalma!%20Gerei%20um%20orçamento%20pelo%20site%20e%20quero%20fechar."
    
    st.markdown(f"""
        <a href="{link_wpp_direto}" target="_blank" style="text-decoration: none;">
            <div style="background-color:#25d366; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold; font-size:18px;">
                💬 CHAMAR NO WHATSAPP AGORA
            </div>
        </a>
        <br>
        <a href="https://instagram.com/djalmalog" target="_blank" style="text-decoration: none;">
            <div style="background-color:#E1306C; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold; font-size:18px;">
                📸 SEGUIR NO INSTAGRAM
            </div>
        </a>
    """, unsafe_allow_html=True)

# Rodapé Institucional
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"""
    <div style="text-align:center; color:#999; font-size:12px; border-top: 1px solid #ddd; padding-top:20px;">
        <p><b>MoveOS 6.0</b> | Sistema de Gestão Djalma Log</p>
        <p>Desenvolvido por Tiago Pinheiro - UFPI Engenharia Mecânica</p>
    </div>
""", unsafe_allow_html=True)
# ==============================================================================
# BLOCO 6: INTEGRAÇÃO COM GOOGLE SHEETS (BANCO DE DADOS)
# ==============================================================================
from streamlit_gsheets import GSheetsConnection

# 6.1 CRIANDO A CONEXÃO
# O Streamlit vai procurar as credenciais nos "Secrets" que vamos configurar.
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Lendo a aba de "Agenda" da planilha
    # Certifique-se de que sua planilha tem uma coluna chamada 'Data' e outra 'Status'
    df_agenda = conn.read(worksheet="Agenda", ttl="5m") 
    
    # Transformando os dados em uma lista para o site usar
    datas_bloqueadas = df_agenda[df_agenda['Status'] == 'Ocupado']['Data'].tolist()
except:
    # Caso a planilha ainda não esteja configurada, usamos dados padrão para o site não cair
    datas_bloqueadas = ["12/03", "15/03", "18/03"]
    st.sidebar.warning("⚠️ Conexão com Banco de Dados pendente.")

# 6.2 FUNÇÃO PARA O GESTOR ATUALIZAR A PLANILHA
def atualizar_banco_dados(nova_data, novo_status):
    # Aqui o código enviaria a nova linha para o Google Sheets
    # Para ativar isso, precisamos das chaves de API do Google
    st.sidebar.info(f"Registrando {nova_data} como {novo_status}...")

