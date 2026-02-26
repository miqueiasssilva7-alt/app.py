import streamlit as st
import pandas as pd

# 1. Configuração para Mobile e Desktop
st.set_page_config(page_title="SmartCommerce AI", layout="centered")

st.title("🚀 SmartCommerce AI")
st.caption("Gestão de Lucro e Meta de Ads")
st.write("---")

# 2. Entrada de Dados (Otimizada para Celular)
st.header("📥 Dados do Produto")
nome_prod = st.text_input("Nome do Produto", "Ex: Fone Bluetooth")

col1, col2 = st.columns(2)
with col1:
    custo_un = st.number_input("Custo Unitário (R$)", min_value=0.01, value=10.00, step=0.01)
    imposto = st.number_input("Imposto (%)", min_value=0.0, value=6.0)
with col2:
    preco_venda = st.number_input("Preço de Venda (R$)", min_value=0.01, value=50.00, step=0.01)
    comissao = st.number_input("Comissão (%)", min_value=0.0, value=12.0)

# 3. Lógica de Cálculo (Original em Inglês)
taxa_fixa = 6.50 if preco_venda < 79 else 0.0
v_imposto = preco_venda * (imposto / 100)
v_comissao = preco_venda * (comissao / 100)
lucro = preco_venda - custo_un - v_imposto - v_comissao - taxa_fixa
margem = (lucro / preco_venda) * 100 if preco_venda > 0 else 0

st.write("---")

# 4. Resultados em Blocos Grandes
st.subheader("📊 Resultado Final")
st.metric("LUCRO LÍQUIDO", f"R$ {lucro:.2f}")
st.metric("MARGEM REAL", f"{margem:.2f}%")

if preco_venda < 79:
    st.warning(f"⚠️ Taxa fixa de R$ 6,50 aplicada.")

st.write("---")

# 5. Meta de Ads (ROAS)
st.header("🎯 Meta de Ads (ROAS)")
if margem > 0:
    roas_eb = 1 / (margem / 100)
    st.info(f"Seu ROAS de Equilíbrio é: **{roas_eb:.2f}**")
    
    roas_atual = st.slider("ROAS atual no painel:", 0.0, 20.0, float(round(roas_eb + 1, 1)))
    
    if roas_atual < roas_eb:
        st.error(f"🔴 PREJUÍZO! Você está perdendo dinheiro.")
    elif roas_atual < (roas_eb * 1.5):
        st.warning("🟡 ALERTA: Lucro baixo.")
    else:
        st.success("🟢 EXCELENTE: Produto lucrativo!")
else:
    st.error("❌ Margem negativa. Não anuncie!")
