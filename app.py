import streamlit as st
import math
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from fpdf import FPDF
from datetime import datetime

# --- CONFIGURAÇÃO VISUAL E TEMA ---
st.set_page_config(page_title="Djalma Log Pro", page_icon="🚚", layout="wide")

# CSS Avançado para dar cara de Aplicativo Moderno
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button {
        background-color: #000033;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        border: none;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #f0f2f6;
        border-radius: 10px 10px 0px 0px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] { background-color: #000033 !important; color: white !important; }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- FUNÇÕES DE APOIO ---
def gerar_pdf_v3(dados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(0, 0, 51)
    pdf.cell(200, 10, txt="DJALMA LOG - ORÇAMENTO OFICIAL", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 8, txt=f"Data da Mudança: {dados['data']}", ln=True)
    pdf.cell(200, 8, txt=f"Origem: {dados['origem']} | Destino: {dados['destino']}", ln=True)
    pdf.cell(200, 8, txt=f"Descrição: {dados['obs']}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="DETALHES LOGÍSTICOS:", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(200, 8, txt=f"- Volume Estimado: {dados['volume']:.2f} m3", ln=True)
    pdf.cell(200, 8, txt=f"- Frota: {dados['viagens']} viagem(ns) no VW Baú", ln=True)
    pdf.cell(200, 8, txt=f"- Equipe: {dados['ajudantes']} ajudantes", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 100, 0)
    pdf.cell(200, 10, txt=f"VALOR TOTAL ESTIMADO: R$ {dados['total']:.2f}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- BANCO DE DATAS (Simulação de Agenda) ---
# Em um sistema real, isso viria de um Banco de Dados
DATAS_OCUPADAS = ["2026-03-15", "2026-03-20", "2026-03-25"]

# --- CONTEÚDO PRINCIPAL (ABAS) ---
tab_orc, tab_agenda, tab_contato = st.tabs(["📝 Novo Orçamento", "📅 Agenda Disponível", "📞 Central de Atendimento"])

with tab_orc:
    st.subheader("Solicite seu Orçamento em Minutos")
    
    col_a, col_b = st.columns(2)
    with col_a:
        origem = st.text_input("📍 Ponto de Partida", placeholder="Cidade, UF")
        data_mudanca = st.date_input("🗓️ Data pretendida", min_value=datetime.now())
    with col_b:
        destino = st.text_input("🏁 Destino Final", placeholder="Cidade, UF")
        tipo_mudanca = st.selectbox("🏠 Tipo da Mudança", ["Residencial", "Comercial", "Apenas Itens Avulsos"])

    st.markdown("### 📦 O que vamos transportar?")
    
    # Inventário Organizado por Categorias
    exp_sala = st.expander("Sala e Escritório")
    exp_quarto = st.expander("Quartos e Camas")
    exp_cozinha = st.expander("Cozinha e Área de Serviço")
    exp_outros = st.expander("✨ Outros Itens (Personalizado)", expanded=True)

    vol_total = 0.0
    
    with exp_sala:
        s1, s2, s3 = st.columns(3)
        vol_total += s1.number_input("Sofá 3 Lug", 0) * 1.42
        vol_total += s2.number_input("Painel/Rack", 0) * 0.50
        vol_total += s3.number_input("Mesa Jantar", 0) * 1.40
        
    with exp_quarto:
        q1, q2, q3 = st.columns(3)
        vol_total += q1.number_input("Cama Casal", 0) * 1.50
        vol_total += q2.number_input("Guarda-Roupa", 0) * 1.80
        vol_total += q3.number_input("Cama Solteiro", 0) * 0.90

    with exp_cozinha:
        c1, c2, c3 = st.columns(3)
        vol_total += c1.number_input("Geladeira", 0) * 1.30
        vol_total += c2.number_input("Fogão", 0) * 0.60
        vol_total += c3.number_input("Máq. Lavar", 0) * 0.70

    with exp_outros:
        st.write("Não achou o que precisava? Adicione aqui:")
        item_extra_nome = st.text_input("Descrição do(s) item(s) extra(s)")
        col_ex1, col_ex2 = st.columns(2)
        qtd_extra = col_ex1.number_input("Quantidade", 0)
        m3_extra = col_ex2.selectbox("Tamanho aproximado", 
                                     [0.2, 0.5, 1.0, 2.0], 
                                     format_func=lambda x: f"{x} m3 (Pequeno a Grande)")
        vol_total += (qtd_extra * m3_extra)
        observacoes = st.text_area("Observações importantes (ex: tem escada, móvel planejado, etc.)")

    if st.button("GERAR ORÇAMENTO PROFISSIONAL"):
        if not origem or not destino or vol_total == 0:
            st.warning("Preencha a rota e adicione pelo menos um item.")
        else:
            with st.spinner("Processando logística..."):
                geolocator = Nominatim(user_agent="djalmalog_v3")
                loc1, loc2 = geolocator.geocode(origem + ", Brasil"), geolocator.geocode(destino + ", Brasil")
                
                if loc1 and loc2:
                    dist = geodesic((loc1.latitude, loc1.longitude), (loc2.latitude, loc2.longitude)).kilometers * 1.25
                    viagens = math.ceil(vol_total / 40.0)
                    ajudantes = max(2, math.ceil(vol_total / 12.0))
                    
                    if dist <= 50:
                        frete = 350.0 * viagens
                        tipo_f = "Local"
                    else:
                        frete = (math.ceil(dist / 50.0) * 50 * 2) * viagens * 3.50
                        tipo_f = "Longa Distância"
                    
                    total = frete + (ajudantes * 100.0)
                    
                    # Dashboard de Resultado
                    st.markdown("---")
                    res_col1, res_col2, res_col3 = st.columns(3)
                    res_col1.metric("Distância", f"{dist:.0f} km")
                    res_col2.metric("Equipe", f"{ajudantes} pessoas")
                    res_col3.metric("Total", f"R$ {total:.2f}")

                    dados_orc = {
                        "origem": origem, "destino": destino, "volume": vol_total,
                        "viagens": viagens, "ajudantes": ajudantes, "total": total,
                        "data": data_mudanca.strftime("%d/%m/%Y"), "obs": observacoes,
                        "tipo_frete": tipo_f
                    }
                    
                    pdf_bytes = gerar_pdf_v3(dados_orc)
                    st.download_button("📩 BAIXAR PDF OFICIAL", pdf_bytes, "DjalmaLog_Orcamento.pdf", "application/pdf")
                else:
                    st.error("Erro no GPS. Verifique os nomes das cidades.")

with tab_agenda:
    st.subheader("Gerenciador de Disponibilidade")
    st.write("Confira os dias em que nossa equipe está livre para sua mudança.")
    
    col_cal, col_info = st.columns([2, 1])
    
    with col_cal:
        # Mostra o calendário apenas para visualização
        st.date_input("Consulte a data no calendário:", datetime.now())
        
    with col_info:
        st.info("🟢 Dias Disponíveis: Segunda a Sábado")
        st.error("🔴 Dias Ocupados: 15/03, 20/03, 25/03")
        st.write("---")
        st.write("**Horário de Funcionamento:**")
        st.write("07:30 às 18:00")

with tab_contato:
    st.subheader("Canais de Atendimento")
    st.write("Fale diretamente com o proprietário ou visite nossas redes.")
    
    c_wpp, c_insta = st.columns(2)
    with c_wpp:
        st.success("✅ WhatsApp: (86) 98862-9083")
        st.link_button("Abrir Conversa no WhatsApp", "https://wa.me/5586988629083")
    with c_insta:
        st.info("📸 Instagram: @djalmalog")
        st.link_button("Ver Perfil no Instagram", "https://instagram.com/djalmalog")

# --- RODAPÉ ---
st.markdown("---")
st.caption("© 2026 Djalma Log - Inteligência em Logística. Desenvolvido por Tiago Pinheiro.")
