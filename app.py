import streamlit as st
import math
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Djalma Log - Orçamentos", page_icon="🚚", layout="centered")

# --- BANCO DE DADOS DE CUBAGEM ---
CATALOGO_MOVEIS = {
    "Caixa Pequena (Livros/Miudezas)": 0.15,
    "Caixa Média (Louças/Diversos)": 0.25,
    "Caixa Grande (Roupas/Cobertores)": 0.40,
    "Geladeira / Freezer": 1.33,
    "Fogão / Cooktop": 0.62,
    "Máquina de Lavar Roupas": 0.67,
    "Sofá 2 Lugares": 0.97,
    "Sofá 3 Lugares": 1.42,
    "Cama de Casal (Box/Padrão)": 1.40,
    "Guarda-Roupa 3 Portas": 1.25,
    "Mesa de Jantar": 1.43,
    "Moto": 3.60
}

# --- FUNÇÕES DE GPS ---
def obter_coordenadas(cidade):
    geolocator = Nominatim(user_agent="djalmalog_web_app")
    try:
        local = geolocator.geocode(cidade + ", Brasil")
        if local: return (local.latitude, local.longitude)
    except:
        return None
    return None

# --- INTERFACE DO SITE ---
st.title("🚚 Djalma Log: Orçamento Inteligente")
st.write("Calcule o valor do seu frete de forma rápida e automática.")

st.header("1. Rota da Mudança 📍")
col1, col2 = st.columns(2)
with col1:
    cidade_origem = st.text_input("Cidade de Origem (ex: Teresina, PI)")
with col2:
    cidade_destino = st.text_input("Cidade de Destino (ex: Timon, MA)")

st.header("2. Leitura por Inteligência Artificial 📷")
st.info("Em breve: Tire uma foto da sua sala e nossa IA fará o inventário sozinha!")
foto = st.file_uploader("Faça upload de um vídeo ou foto do cômodo (Versão Beta)", type=["jpg", "png", "mp4"])
if foto:
    st.warning("A imagem foi recebida, mas o motor visual da IA está em fase de treinamento. Por favor, use o inventário manual abaixo.")

st.header("3. Inventário Manual 📦")
st.write("Selecione a quantidade de itens que serão transportados:")

volume_total = 0.0

# Cria botões de + e - para cada móvel de forma bonita
for nome_movel, m3 in CATALOGO_MOVEIS.items():
    qtd = st.number_input(nome_movel, min_value=0, max_value=20, step=1)
    volume_total += qtd * m3

# --- BOTÃO DE CÁLCULO ---
if st.button("Calcular Orçamento Completo", type="primary"):
    if not cidade_origem or not cidade_destino:
        st.error("Por favor, preencha as cidades de origem e destino.")
    elif volume_total == 0:
        st.error("Por favor, adicione pelo menos um item ao inventário.")
    else:
        with st.spinner("Conectando aos satélites e calculando a logística..."):
            coord_origem = obter_coordenadas(cidade_origem)
            coord_destino = obter_coordenadas(cidade_destino)
            
            if not coord_origem or not coord_destino:
                st.error("Não foi possível encontrar as cidades no GPS. Verifique a ortografia e a sigla do estado.")
            else:
                distancia_ida = geodesic(coord_origem, coord_destino).kilometers * 1.25
                
                # Regras de Negócio
                capacidade_caminhao = 40.0
                taxa_minima = 350.00
                valor_km = 3.50
                diaria_ajudante = 100.00
                
                num_viagens = math.ceil(volume_total / capacidade_caminhao)
                if num_viagens == 0: num_viagens = 1
                num_ajudantes = max(2, math.ceil(volume_total / 10.0))
                
                # Exibição dos Resultados
                st.success("Orçamento gerado com sucesso!")
                
                st.subheader("📦 Resumo da Carga")
                st.write(f"**Volume Total:** {volume_total:.2f} m³")
                st.write(f"**Caminhões/Viagens necessárias:** {num_viagens}")
                st.write(f"**Equipe de Ajudantes:** {num_ajudantes} pessoas")
                
                st.subheader("💰 Resumo Financeiro")
                if distancia_ida <= 50:
                    custo_rodagem = taxa_minima * num_viagens
                    st.write(f"**Tipo de Frete:** Local/Metropolitano")
                    st.write(f"**Custo do Caminhão:** R$ {custo_rodagem:.2f}")
                else:
                    distancia_cobrada = math.ceil(distancia_ida / 50.0) * 50
                    distancia_total_frota = (distancia_cobrada * 2) * num_viagens
                    custo_rodagem = distancia_total_frota * valor_km
                    st.write(f"**Tipo de Frete:** Interestadual / Longa Distância")
                    st.write(f"**Distância Cobrada:** {distancia_total_frota} km totais faturados")
                    st.write(f"**Custo de Rodagem:** R$ {custo_rodagem:.2f}")
                
                custo_equipe = num_ajudantes * diaria_ajudante
                valor_final = custo_rodagem + custo_equipe
                
                st.write(f"**Custo da Equipe:** R$ {custo_equipe:.2f}")
                st.markdown(f"### 🏆 VALOR FINAL SUGERIDO: R$ {valor_final:.2f}")
                st.balloons() # Efeito visual comemorativo do Streamlit