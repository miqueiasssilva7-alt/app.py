import streamlit as st
import pandas as pd

# 1. Configuração para dispositivos móveis
st.set_page_config(page_title="SmartCommerce Mobile", layout="centered")

st.title("🚀 SmartCommerce AI")
st.write("---")

# 2. Inputs - No celular, é melhor deixar um abaixo do outro
st.header("📥 Entrada de Dados")
nome_prod = st.text_input("Nome do Produto", "Produto Exemplo")

# Usando colunas apenas para inputs curtos
col_a, col_b = st.columns(2)
with col_a:
    custo_un = st.number_input("Custo Unitário (R$)", min_value=0.01, value=12.05)
    imposto = st.number_input("Imposto (%)", value=6.0)
with col_b:
    preco_venda = st.number_input("Preço de Venda (R$)", min_value=0.01, value=26.06)
    comissao = st.number_input("Comissão (%)", value=12.0)

# 3. Lógica de Cálculo
taxa_fixa = 6.50 if preco_venda < 79 else 0.0
v_imposto = preco_venda * (imposto / 100)
v_comissao = preco_venda * (comissao / 100)
lucro = preco_venda - custo_un - v_imposto - v_comissao - taxa_fixa
margem = (lucro / preco_venda) * 100 if preco_venda > 0 else 0

st.write("---")

# 4. Resultados Grandes para leitura fácil no celular
st.header("📊 Resultado Real")

# Em vez de colunas pequenas, vamos usar "cards" ou métricas grandes
st.metric("LUCRO NO BOLSO", f"R$ {lucro:.2f}")
st.metric("MARGEM REAL", f"{margem:.2f}%")

if preco_venda < 79:
    st.warning(f"⚠️ Atenção: Taxa fixa de R$ 6,50 aplicada (Venda < R$ 79)")

st.write("---")

# 5. Seção de ADS (ROAS) otimizada
st.header("🎯 Meta de Ads (ROAS)")

if margem > 0:
    roas_eb = 1 / (margem / 100)
    st.info(f"Seu ROAS de Equilíbrio é: **{roas_eb:.2f}**")
    
    # Slider maior para facilitar o toque no celular
    roas_atual = st.select_slider(
        "Quanto está o ROAS no seu painel hoje?",
        options=[round(i * 0.5, 1) for i in range(0, 41)], # Vai de 0 a 20
        value=round(roas_eb + 1, 1)
    )
    
    if roas_atual < roas_eb:
        st.error(f"🔴 PREJUÍZO! Você precisa de pelo menos {roas_eb:.2f}")
    elif roas_atual < (roas_eb * 1.5):
        st.warning("🟡 CUIDADO: Lucro muito baixo.")
    else:
        st.success("🟢 EXCELENTE: Pode escalar o investimento!")
else:
    st.error("❌ Margem negativa. Não anuncie!")
