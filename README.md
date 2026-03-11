# 🚚 MoveOS: Sistema de Gestão e Orçamentação Logística (Djalma Log)

![Status](https://img.shields.io/badge/Status-Produção-success)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B)
![Engenharia](https://img.shields.io/badge/Foco-Engenharia%20de%20Carga-orange)

O **MoveOS** (versão 6.0) é uma aplicação web completa desenvolvida para automatizar e otimizar o processo de orçamentação e planejamento de cargas da **Djalma Log**, uma empresa de fretes e mudanças. 

O sistema substitui o orçamento manual por um motor de cálculo automatizado que cruza dados de geolocalização (GPS), volumetria de carga (cubagem em m³) e regras de negócio financeiras para gerar propostas comerciais em PDF com alta precisão.

## 🎯 Principais Funcionalidades

* **📍 Roteirização Inteligente:** Integração com a API do ArcGIS (via Geopy) para cálculo preciso de distâncias em quilômetros, aplicando fatores de correção para trajetos rodoviários.
* **📦 Motor de Cubagem Dinâmico:** Banco de dados interno com as medidas volumétricas (m³) padronizadas de móveis e eletrodomésticos, separados por ambientes (Sala, Quarto, Cozinha, Frágeis e Especiais).
* **📊 Dashboard de Ocupação:** Renderização em tempo real (usando Plotly) da ocupação espacial do caminhão (VW Baú 40m³). O sistema alerta visualmente sobre espaço livre ou sobrecarga.
* **📄 Geração Automática de Contratos (PDF):** Compilação de todos os dados do cliente, inventário e taxas extras em um documento PDF profissional (via FPDF) pronto para envio via WhatsApp.
* **⚙️ Precificação Algorítmica:** Cálculo que considera:
    * Frete Urbano vs. Frete de Longa Distância.
    * Taxas de insalubridade (escadas).
    * Serviços de valor agregado (embalagem profissional por m³ e desmontagem técnica).
    * Dimensionamento de equipe (cálculo de ajudantes necessários com base no volume total).
* **🔒 Área do Gestor:** Painel restrito por senha para gerenciamento de disponibilidade da frota e atualização da agenda de serviços.

## 🏗️ Arquitetura e Tecnologias

O projeto foi construído utilizando as seguintes tecnologias e bibliotecas:

* **Front-end & Lógica UI:** [Streamlit](https://streamlit.io/) (com injeção de CSS personalizado para UI/UX avançada).
* **Processamento de Dados e Matemática:** `math`, `pandas`
* **Geolocalização:** `geopy` (ArcGIS geocoder)
* **Geração de Documentos:** `fpdf`
* **Visualização de Dados:** `plotly.graph_objects`

## 🚀 Como Executar o Projeto Localmente
Acessar link:
https://move-os-djalma-log.streamlit.app/
