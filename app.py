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
                
                # =======================================================
                # 🛑 TRAVA COMERCIAL: CARGA GIGANTE INTERESTADUAL
                # =======================================================
                if volume_total > capacidade_caminhao and distancia_ida > 50:
                    st.warning(f"⚠️ **Carga Especial Detectada ({volume_total:.2f} m³)**")
                    st.write("O volume da sua mudança excede a capacidade de um caminhão padrão (40 m³) para viagens de longa distância.")
                    st.info("📲 Para logísticas desse porte, precisamos montar uma frota personalizada com mais veículos. Entre em contato direto com a nossa equipe!")
                    
                    # Botão do WhatsApp (com o número da Djalma Log)
                    link_wpp = "https://wa.me/5586988629083?text=Olá!%20Fiz%20um%20orçamento%20no%20site%20e%20minha%20mudança%20deu%20carga%20especial."
                    st.link_button("Negociar via WhatsApp", link_wpp)
                    
                else:
                    # =======================================================
                    # ✅ CÁLCULO NORMAL (Dentro da capacidade ou frete local)
                    # =======================================================
                    num_viagens = math.ceil(volume_total / capacidade_caminhao)
                    if num_viagens == 0: num_viagens = 1
                    num_ajudantes = max(2, math.ceil(volume_total / 10.0))
                    
                    st.success("Orçamento gerado com sucesso!")
                    
                    st.subheader("📦 Resumo da Carga")
                    st.write(f"**Volume Total:** {volume_total:.2f} m³")
                    st.write(f"**Caminhões/Viagens necessárias:** {num_viagens}")
                    st.write(f"**Equipe de Ajudantes:** {num_ajudantes} pessoas")
                    
                    st.subheader("💰 Resumo Financeiro")
                    if distancia_ida <= 50:
                        custo_rodagem = taxa_minima * num_viagens
                        st.write(f"**Tipo de Frete:** Local / Metropolitano")
                        st.write(f"**Custo da Frota:** R$ {custo_rodagem:.2f}")
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
                    st.balloons()
