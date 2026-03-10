import streamlit as st
import math
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from fpdf import FPDF
from datetime import datetime

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="Djalma Log - Gestão de Fretes", page_icon="🚚", layout="wide")

# CSS para tornar o site um "Dashboard" Profissional
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .main-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #000033 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        height: 3.5em !important;
    }
    h1, h2, h3 { color: #000033; font-family: 'Segoe UI', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# --- FUNÇÃO GERADORA DE PDF V4 ---
def gerar_pdf_v4(d):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(0, 0, 51)
    pdf.cell(200, 10, txt="DJALMA LOG - PROPOSTA COMERCIAL", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 8, txt=f"Data Solicitada: {d['data']} | Tipo: {d['tipo_m']}", ln=True)
    pdf.cell(200, 8, txt=f"Rota: {d['origem']} -> {d['destino']}", ln=True)
    pdf.cell(200, 8, txt=f"Servicos Adicionais: {d['servicos']}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="ESPECIFICACOES DA CARGA:", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(200, 8, txt=f"- Volume Total: {d['volume']:.2f} m3", ln=True)
    pdf.cell(200, 8, txt=f"- Equipe: {d['ajudantes']} ajudantes | Viagens: {d['viagens']}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 100, 0)
    pdf.cell(200, 10, txt=f"INVESTIMENTO TOTAL: R$ {d['total']:.2f}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 9)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(0, 5, txt=f"Observacoes do Cliente: {d['obs']}")
    return pdf.output(dest='S').encode('latin-1')

# --- INTERFACE PRINCIPAL ---
tab1, tab2, tab3 = st.tabs(["📋 Orçamento Detalhado", "📅 Agenda", "📞 Contato"])

with tab1:
    st.title("Sistema de Orçamento Inteligente 🚚")
    
    with st.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        col_r1, col_r2, col_r3 = st.columns([2, 2, 1])
        origem = col_r1.text_input("📍 Origem", placeholder="Teresina, PI")
        destino = col_r2.text_input("🏁 Destino", placeholder="Parnaíba, PI")
        data_m = col_r3.date_input("🗓️ Data", min_value=datetime.now())
        st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("🛠️ Serviços e Preferências")
    c_s1, c_s2 = st.columns(2)
    with c_s1:
        tipo_m = st.selectbox("Tipo de Mudança", ["Residencial", "Comercial", "Industrial"])
        embalagem = st.toggle("Preciso que a Djalma Log EMBALE meus pertences", help="Adiciona custo de materiais e mão de obra extra.")
    with c_s2:
        desmontagem = st.toggle("Preciso de DESMONTAGEM de móveis")
        escadas = st.toggle("O local possui ESCADAS ou subidas difíceis?")

    st.subheader("📦 Inventário Completo")
    
    # Categorias com os itens que você sentiu falta
    cat1, cat2, cat3 = st.columns(3)
    
    vol_t = 0.0
    with cat1:
        st.write("**Eletrônicos e Sala**")
        vol_t += st.number_input("TVs (LCD/LED)", 0) * 0.50
        vol_t += st.number_input("Sofás", 0) * 1.40
        vol_t += st.number_input("Painéis/Racks", 0) * 0.60
    
    with cat2:
        st.write("**Delicados e Vidros**")
        vol_t += st.number_input("Espelhos Grandes", 0) * 0.30
        vol_t += st.number_input("Tampos de Vidro", 0) * 0.40
        vol_t += st.number_input("Cristaleiras", 0) * 1.20
        
    with cat3:
        st.write("**Eletros e Quartos**")
        vol_t += st.number_input("Geladeiras", 0) * 1.30
        vol_t += st.number_input("Camas Box", 0) * 1.50
        vol_t += st.number_input("Guarda-Roupas", 0) * 1.80

    st.write("---")
    st.write("**✨ Itens Não Listados / Outros**")
    col_o1, col_o2 = st.columns([3, 1])
    obs_extra = col_o1.text_input("Descreva o item extra (Ex: Piano, Mesa de Sinuca...)")
    vol_extra = col_o2.number_input("Volume Extra (m³)", 0.0, step=0.5)
    vol_t += vol_extra
    
    obs_geral = st.text_area("Observações Especiais para a Equipe")

    if st.button("GERAR PROPOSTA COMERCIAL"):
        if not origem or not destino or vol_t == 0:
            st.error("Dados insuficientes para calcular.")
        else:
            with st.spinner("Calculando Logística..."):
                geolocator = Nominatim(user_agent="djalmalog_v4")
                loc1, loc2 = geolocator.geocode(origem + ", Brasil"), geolocator.geocode(destino + ", Brasil")
                
                if loc1 and loc2:
                    dist = geodesic((loc1.latitude, loc1.longitude), (loc2.latitude, loc2.longitude)).kilometers * 1.25
                    viagens = math.ceil(vol_t / 40.0)
                    ajudantes = max(2, math.ceil(vol_t / 10.0))
                    
                    # LOGICA DE PREÇO V4
                    # Frete base
                    if dist <= 50:
                        custo_f = 350.0 * viagens
                    else:
                        custo_f = (math.ceil(dist / 50.0) * 50 * 2) * viagens * 3.50
                    
                    # Adicionais
                    taxa_embalagem = (vol_t * 25.0) if embalagem else 0 # R$ 25 por m3 embalado
                    taxa_dificuldade = 150.0 if escadas else 0
                    custo_equipe = ajudantes * 100.0
                    
                    total_geral = custo_f + taxa_embalagem + taxa_dificuldade + custo_equipe
                    
                    # Dashboard de Resultado
                    st.success("Cálculo Finalizado!")
                    d1, d2, d3, d4 = st.columns(4)
                    d1.metric("Distância Ida", f"{dist:.0f} km")
                    d2.metric("Ajudantes", f"{ajudantes}")
                    d3.metric("Volume", f"{vol_t:.1f} m³")
                    d4.metric("TOTAL", f"R$ {total_geral:.2f}")
                    
                    # Texto de Serviços para o PDF
                    svs = []
                    if embalagem: svs.append("Embalagem")
                    if desmontagem: svs.append("Desmontagem")
                    if escadas: svs.append("Subida por Escada")
                    svs_txt = ", ".join(svs) if svs else "Apenas transporte"

                    dados_pdf = {
                        "origem": origem, "destino": destino, "volume": vol_t,
                        "viagens": viagens, "ajudantes": ajudantes, "total": total_geral,
                        "data": data_m.strftime("%d/%m/%Y"), "obs": obs_geral,
                        "tipo_m": tipo_m, "servicos": svs_txt
                    }
                    
                    pdf_out = gerar_pdf_v4(dados_pdf)
                    st.download_button("📩 Baixar Proposta em PDF", pdf_out, "Proposta_DjalmaLog.pdf", "application/pdf")
                else:
                    st.error("GPS não localizou as cidades.")

with tab2:
    st.subheader("Disponibilidade da Frota")
    st.info("O caminhão VW Baú 40m³ está disponível para novas mudanças!")
    st.write("Datas bloqueadas: 15/03, 20/03.")

with tab3:
    st.subheader("Fale com a Djalma Log")
    st.write("📲 WhatsApp: (86) 98862-9083")
    st.link_button("Chamar no WhatsApp", "https://wa.me/5586988629083")
