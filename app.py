import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração de Página
st.set_page_config(page_title="Smart Commerce", layout="centered")

# --- CABEÇALHO ---
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

# --- LÓGICA DE AUTOMATIZAÇÃO DA FAIXA DE PREÇO ---
faixas_venda = [
    "R$ 0 a R$ 18,99", 
    "R$ 19 a R$ 48,99", 
    "R$ 49 a R$ 78,99", 
    "R$ 79 a R$ 99,99", 
    "R$ 100 a R$ 119,99", 
    "R$ 120 a R$ 149,99", 
    "R$ 150 a R$ 199,99", 
    "A partir de R$ 200"
]

idx_automatico = 0
if preco_venda is not None:
    if preco_venda <= 18.99: idx_automatico = 0
    elif preco_venda <= 48.99: idx_automatico = 1
    elif preco_venda <= 78.99: idx_automatico = 2
    elif preco_venda <= 99.99: idx_automatico = 3
    elif preco_venda <= 119.99: idx_automatico = 4
    elif preco_venda <= 149.99: idx_automatico = 5
    elif preco_venda <= 199.99: idx_automatico = 6
    else: idx_automatico = 7

# --- SEÇÃO DE FRETE ---
st.write("---")
st.subheader("🚚 Configuração de Frete")

tabela_frete = {
    "Até 0,3 kg": [5.65, 6.55, 7.75, 12.35, 14.35, 16.45, 18.45, 20.95],
    "De 0,3 a 0,5 kg": [5.95, 6.65, 7.85, 13.25, 15.45, 17.65, 19.85, 22.55],
    "De 0,5 a 1 kg": [6.05, 6.75, 7.95, 13.85, 16.15, 18.45, 20.75, 23.65],
    "De 1 a 1,5 kg": [6.15, 6.85, 8.05, 14.15, 16.45, 18.85, 21.15, 24.65],
    "De 1,5 a 2 kg": [6.25, 6.95, 8.15, 14.45, 16.85, 19.25, 21.65, 24.65],
    "De 2 a 3 kg": [6.35, 7.95, 8.55, 15.75, 18.35, 21.05, 23.65, 26.25],
    "De 3 a 4 kg": [6.45, 8.15, 8.95, 17.05, 19.85, 22.65, 25.55, 28.35],
    "De 4 a 5 kg": [6.55, 8.35, 9.75, 18.45, 21.55, 24.65, 27.75, 30.75],
    "De 5 a 6 kg": [6.65, 8.55, 9.95, 25.45, 28.55, 32.65, 35.75, 39.75],
    "De 9 a 11 kg": [7.05, 9.55, 10.95, 41.25, 48.05, 54.95, 61.75, 68.65],
    "De 20 a 25 kg": [7.65, 10.95, 12.15, 64.05, 75.05, 84.75, 95.35, 105.95],
    "De 70 a 80 kg": [8.35, 12.15, 13.35, 82.25, 97.05, 109.85, 122.45, 132.25]
}

col_f1, col_f2 = st.columns(2)
with col_f1:
    # O index=idx_automatico faz a mágica de selecionar sozinho baseado no preço
    sel_faixa_venda = st.selectbox("Faixa de Preço (Auto):", faixas_venda, index=idx_automatico)
with col_f2:
    sel_peso = st.selectbox("Peso do Produto:", list(tabela_frete.keys()))

idx_venda = faixas_venda.index(sel_faixa_venda)
frete_val = tabela_frete[sel_peso][idx_venda]

# 3. Lógica de Cálculo
if custo_un and preco_venda:
    v_imposto = preco_venda * (imposto / 100) if imposto else 0
    v_comissao = preco_venda * (comissao / 100) if comissao else 0
    
    lucro = preco_venda - custo_un - v_imposto - v_comissao - frete_val
    margem = (lucro / preco_venda) * 100 if preco_venda > 0 else 0
    
    st.write("---")
    
    # 4. Resultados e Análise
    st.subheader("📊 Análise de Composição")
    
    if margem >= 20:
        st.success("🚀 **ESTRATÉGIA VENCEDORA! DECOLOUE!**")
        st.toast("Rumo ao topo!", icon="🚀")

    col_res1, col_res2, col_res3 = st.columns(3)
    col_res1.metric("LUCRO LÍQUIDO", f"R$ {lucro:.2f}")
    col_res2.metric("MARGEM REAL", f"{margem:.2f}%")
    col_res3.metric("FRETE APLICADO", f"R$ {frete_val:.2f}")

    # --- GRÁFICO ---
    dados_grafico = {
        "Categoria": ["Custo Unitário", "Imposto", "Comissão", "Frete", "Lucro Líquido"],
        "Valores": [custo_un, v_imposto, v_comissao, frete_val, max(0, lucro)]
    }
    df_pizza = pd.DataFrame(dados_grafico)
    fig = px.pie(df_pizza, values='Valores', names='Categoria', hole=0.4,
                 color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig, use_container_width=True)
    
    # 5. Meta de Ads (ROAS)
    st.header("🎯 Meta de Ads (ROAS)")
    if margem > 0:
        roas_eb = 1 / (margem / 100)
        st.info(f"Seu ROAS de Equilíbrio é: **{roas_eb:.2f}**")
        roas_atual = st.slider("Qual o ROAS atual da campanha?", 0.1, 20.0, float(round(roas_eb + 1, 1)))
        
        if roas_atual < roas_eb:
            st.error(f"🔴 Prejuízo detectado no Ads.")
        else:
            st.success(f"🟢 Operação Lucrativa")
else:
    st.info("💡 Insira o Preço de Venda para que o frete seja calculado automaticamente.")
