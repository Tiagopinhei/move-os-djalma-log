import streamlit as st
import math
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from fpdf import FPDF

# --- CONFIGURAÇÃO E ESTÉTICA DA PÁGINA ---
st.set_page_config(page_title="Djalma Log - Orçamentos", page_icon="🚚", layout="centered")

# Injeção de CSS para deixar o site com cara de Aplicativo Premium
st.markdown("""
    <style>
    /* Cor do botão principal de Calcular */
    div.stButton > button:first-child {
        background-color: #000033;
        color: white;
        border-radius: 8px;
        width: 100%;
        font-weight: bold;
        border: none;
        padding: 10px;
    }
    div.stButton > button:first-child:hover {
        background-color: #000066;
        color: white;
    }
    /* Esconder o menu superior do Streamlit e rodapé */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    /* Destacar os cabeçalhos com a cor da empresa */
    h1, h2, h3 {
        color: #000033;
    }
    </style>
""", unsafe_allow_html=True)

# --- FUNÇÃO GERADORA DE PDF ---
def criar_pdf_orcamento(origem, destino, volume, viagens, ajudantes, tipo_frete, valor_total):
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(0, 0, 51) # Azul escuro
    pdf.cell(200, 10, txt="DJALMA LOG FRETES E MUDANCAS", ln=True, align='C')
    
    pdf.set_font("Arial", '', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(200, 6, txt="CNPJ: 12.214.673/0001-23 | Telefone: (86) 98862-9083", ln=True, align='C')
    pdf.ln(10) # Pular linha
    
    # Corpo do Orçamento
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 10, txt="RESUMO DO ORCAMENTO", ln=True)
    
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 8, txt=f"Origem: {origem} | Destino: {destino}", ln=True)
    pdf.cell(200, 8, txt=f"Volume Estimado da Carga: {volume:.2f} m3", ln=True)
    pdf.cell(200, 8, txt=f"Caminhoes / Viagens: {viagens}", ln=True)
    pdf.cell(200, 8, txt=f"Mao de Obra Especializada: {ajudantes} ajudantes", ln=True)
    pdf.cell(200, 8, txt=f"Categoria de Frete: {tipo_frete}", ln=True)
    pdf.ln(5)
    
    # Valor Final
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 102, 0) # Verde para o valor
    pdf.cell(200, 10, txt=f"VALOR TOTAL DO INVESTIMENTO: R$ {valor_total:.2f}", ln=True)
    
    pdf.ln(15)
    pdf.set_font("Arial", 'I', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(200, 10, txt='"Compromisso com qualidade, seguranca e pontualidade."', ln=True, align='C')
    
    return pdf.output(dest='S').encode('latin-1')

# --- BANCO DE DADOS DE CUBAGEM ---
CATALOGO_MOVEIS = {
    "Caixa Pequena (Livros)": 0.15,
    "Caixa Média (Louças)": 0.25,
    "Caixa Grande (Roupas)": 0.40,
    "Geladeira / Freezer": 1.33,
    "Fogão / Cooktop": 0.62,
    "Máquina de Lavar Roupas": 0.67,
    "Sofá 2 Lugares": 0.97,
    "Sofá 3 Lugares": 1.42,
    "Cama de Casal (Padrão/Box)": 1.40,
    "Guarda-Roupa 3 Portas": 1.25,
    "Mesa de Jantar": 1.43,
    "Moto": 3.60
}

def obter_coordenadas(cidade):
    geolocator = Nominatim(user_agent="djalmalog_web_app")
    try:
        local = geolocator.geocode(cidade + ", Brasil")
        if local: return (local.latitude, local.longitude)
    except:
        return None
    return None

# --- INTERFACE DO SITE ---
st.title("🚚 Djalma Log: Orçamento Expresso")
st.markdown("---")

st.subheader("1. Rota da Mudança 📍")
col1, col2 = st.columns(2)
with col1:
    cidade_origem = st.text_input("Cidade de Origem (ex: Teresina, PI)")
with col2:
    cidade_destino = st.text_input("Cidade de Destino (ex: Timon, MA)")

st.markdown("---")
st.subheader("2. Inventário de Carga 📦")
st.write("Adicione a quantidade dos itens abaixo para dimensionarmos o caminhão:")

# Layout mais bonito para os botões usando colunas
volume_total = 0.0
moveis_cols = st.columns(3)
idx = 0
for nome_movel, m3 in CATALOGO_MOVEIS.items():
    with moveis_cols[idx % 3]:
        qtd = st.number_input(nome_movel, min_value=0, max_value=20, step=1)
        volume_total += qtd * m3
    idx += 1

st.markdown("---")

# --- BOTÃO DE CÁLCULO ---
if st.button("CALCULAR FRETE", type="primary"):
    if not cidade_origem or not cidade_destino:
        st.error("Por favor, preencha as cidades de origem e destino.")
    elif volume_total == 0:
        st.error("Por favor, adicione pelo menos um item ao inventário.")
    else:
        with st.spinner("Analisando rotas e dimensionando a frota..."):
            coord_origem = obter_coordenadas(cidade_origem)
            coord_destino = obter_coordenadas(cidade_destino)
            
            if not coord_origem or not coord_destino:
                st.error("Não foi possível encontrar as cidades no GPS. Verifique a ortografia.")
            else:
                distancia_ida = geodesic(coord_origem, coord_destino).kilometers * 1.25
                
                capacidade_caminhao = 40.0
                taxa_minima = 350.00
                valor_km = 3.50
                diaria_ajudante = 100.00
                
                # TRAVA COMERCIAL
                if volume_total > capacidade_caminhao and distancia_ida > 50:
                    st.warning(f"⚠️ **Carga Especial Detectada ({volume_total:.2f} m³)**")
                    st.write("O volume excede a capacidade de um caminhão padrão para longa distância.")
                    link_wpp = "https://wa.me/5586988629083?text=Olá!%20Minha%20mudança%20deu%20carga%20especial."
                    st.link_button("Negociar Frota via WhatsApp", link_wpp)
                    
                else:
                    num_viagens = math.ceil(volume_total / capacidade_caminhao)
                    if num_viagens == 0: num_viagens = 1
                    num_ajudantes = max(2, math.ceil(volume_total / 10.0))
                    
                    if distancia_ida <= 50:
                        custo_rodagem = taxa_minima * num_viagens
                        tipo_frete = "Local / Metropolitano"
                    else:
                        distancia_cobrada = math.ceil(distancia_ida / 50.0) * 50
                        custo_rodagem = (distancia_cobrada * 2) * num_viagens * valor_km
                        tipo_frete = "Interestadual / Longa Distância"
                    
                    custo_equipe = num_ajudantes * diaria_ajudante
                    valor_final = custo_rodagem + custo_equipe
                    
                    # Interface de Sucesso
                    st.success("Orçamento gerado com sucesso!")
                    
                    colA, colB = st.columns(2)
                    with colA:
                        st.info(f"**📦 Volume Total:** {volume_total:.2f} m³\n\n**🚛 Frota:** {num_viagens} caminhão(ões)\n\n**👷 Equipe:** {num_ajudantes} pessoas")
                    with colB:
                        st.success(f"**💰 VALOR FINAL:**\n\n### R$ {valor_final:.2f}\n\n*Categoria: {tipo_frete}*")
                    
                    st.balloons()
                    
                    # --- BOTÃO MÁGICO DO PDF ---
                    st.markdown("---")
                    pdf_bytes = criar_pdf_orcamento(
                        cidade_origem, cidade_destino, volume_total, num_viagens, 
                        num_ajudantes, tipo_frete, valor_final
                    )
                    
                    st.download_button(
                        label="📄 Baixar Orçamento Oficial em PDF",
                        data=pdf_bytes,
                        file_name=f"Orcamento_DjalmaLog.pdf",
                        mime="application/pdf",
                    )
