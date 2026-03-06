import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração de Página
st.set_page_config(page_title="Smart Commerce", layout="centered")

# --- CABEÇALHO PERSONALIZADO ---
st.title("🚀 Smart Commerce")
st.markdown("### Omni Stratagem LTDA")
st.caption("Gestão de Lucro e Meta de Ads")
st.write("---")

# 2. Entrada de Dados Base
st.header("📥 Dados do Produto")
nome_prod = st.text_input("Nome do Produto", placeholder="Ex: Fone Bluetooth")

col1, col2 = st.columns(2)
with col1:
    custo_un = st.number_input("Custo Unitário (R$)", min_value=0.0, step=0.01, value=None, placeholder="0,00")
    imposto = st.number_input("Imposto (%)", min_value=0.0, step=0.1, value=None, placeholder="6.0")
with col2:
    preco_venda = st.number_input("Preço de Venda (R$)", min_value=0.0, step=0.01, value=None, placeholder="0,00")
    comissao = st.number_input("Comissão (%)", min_value=0.0, step=0.1, value=None, placeholder="12.0")

# --- SEÇÃO DE TAXA FIXA E FRETE ---
st.write("---")
col_tax1, col_tax2 = st.columns(2)

with col_tax1:
    st.subheader("📌 Taxa Fixa")
    opcoes_taxas = {
        "Nenhuma": 0.0,
        "ML: R$ 6,25": 6.25,
        "ML: R$ 6,50": 6.50,
        "ML: R$ 6,75": 6.75,
        "Shopee: R$ 4,00": 4.00,
        "Shopee: R$ 18,00": 18.00,
        "Shopee: R$ 26,00": 26.00
    }
    escolha_taxa = st.selectbox("Selecione a Taxa Fixa:", options=list(opcoes_taxas.keys()))
    taxa_fixa_val = opcoes_taxas[escolha_taxa]

with col_tax2:
    st.subheader("🚚 Frete (Peso/Preço)")
    # Dados extraídos da imagem enviada
    faixas_venda = ["R$ 100 a R$ 119,99", "R$ 120 a R$ 149,99", "R$ 150 a R$ 199,99", "A partir de R$ 200"]
    
    tabela_frete = {
        "Até 0,3 kg": [14.35, 16.45, 18.45, 20.95],
        "De 0,3 a 0,5 kg": [15.45, 17.65, 19.85, 22.55],
        "De 0,5 a 1 kg": [16.15, 18.45, 20.75, 23.65],
        "De 1 a 1,5 kg": [16.45, 18.85, 21.15, 24.65],
        "De 1,5 a 2 kg": [16.85, 19.25, 21.65, 24.65],
        "De 2 a 3 kg": [18.35, 21.05, 23.65, 26.25],
        "De 3 a 4 kg": [19.85, 22.65, 25.55, 28.35],
        "De 4 a 5 kg": [21.55, 24.65, 27.75, 30.75],
        "De 5 a 6 kg": [28.55, 32.65, 35.75, 39.75],
        "De 9 a 11 kg": [48.05, 54.95, 61.75, 68.65],
        "De 20 a 25 kg": [75.05, 84.75, 95.35, 105.95],
        "De 70 a 80 kg": [97.05, 109.85, 122.45, 132.25]
    }
    
    sel_faixa_venda = st.selectbox("Faixa de Venda:", faixas_venda)
    sel_peso = st.selectbox("Peso do Produto:", list(tabela_frete.keys()))
    
    idx_venda = faixas_venda.index(sel_faixa_venda)
    frete_val = tabela_frete[sel_peso][idx_venda]

# 3. Lógica de Cálculo
if custo_un and preco_venda:
    v_imposto = preco_venda * (imposto / 100) if imposto else 0
    v_comissao = preco_venda * (comissao / 100) if comissao else 0
    
    # Cálculo do Lucro incluindo o Frete
    lucro = preco_venda - custo_un - v_imposto - v_comissao - taxa_fixa_val - frete_val
    margem = (lucro / preco_venda) * 100 if preco_venda > 0 else 0
    
    st.write("---")
    
    # 4. Resultados e Gráfico
    st.subheader("📊 Análise de Composição")
    
    if margem >= 20:
        st.balloons()
        st.success("🏆 **ESTRATÉGIA VENCEDORA DETECTADA!**")

    col_res1, col_res2, col_res3 = st.columns(3)
    col_res1.metric("LUCRO LÍQUIDO", f"R$ {lucro:.2f}")
    col_res2.metric("MARGEM REAL", f"{margem:.2f}%")
    col_res3.metric("FRETE APLICADO", f"R$ {frete_val:.2f}")

    # --- CRIAÇÃO DO GRÁFICO DE PIZZA ---
    dados_grafico = {
        "Categoria": ["Custo Produto", "Imposto", "Comissão", "Taxa Fixa", "Frete", "Lucro Líquido"],
        "Valores": [custo_un, v_imposto, v_comissao, taxa_fixa_val, frete_val, max(0, lucro)]
    }
    df_pizza = pd.DataFrame(dados_grafico)
    
    fig = px.pie(df_pizza, values='Valores', names='Categoria', 
                 title="Distribuição do Preço de Venda",
                 color_discrete_sequence=px.colors.sequential.RdBu,
                 hole=0.4)
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.write("---")

    # 5. Meta de Ads (ROAS)
    st.header("🎯 Meta de Ads (ROAS)")
    if margem > 0:
        roas_eb = 1 / (margem / 100)
        st.info(f"Seu ROAS de Equilíbrio é: **{roas_eb:.2f}**")
        roas_atual = st.slider("Quanto está o ROAS no painel?", 0.0, 20.0, float(round(roas_eb + 1, 1)))
        
        if roas_atual < roas_eb:
            st.error(f"🔴 PREJUÍZO! Ponto de corte: {roas_eb:.2f}")
        else:
            st.success("🟢 OPERAÇÃO LUCRATIVA")
    else:
        st.error("❌ Margem negativa. Ajuste o preço ou custos para calcular o ROAS.")

else:
    st.info("💡 Insira o Custo e o Preço de Venda para gerar a análise.")
