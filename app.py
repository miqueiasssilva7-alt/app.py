import streamlit as st
import pandas as pd

# Configuração da Interface
st.set_page_config(page_title="SmartCommerce AI - Dashboard", layout="wide")

# Estilização básica para melhorar a leitura
st.markdown("""
    <style>
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 SmartCommerce AI: Gestão de Lucro & Ads")
st.info("Este app calcula sua margem real e define o limite de gastos com anúncios (ROAS).")

# --- BARRA LATERAL (INPUTS) ---
st.sidebar.header("📥 Dados do Produto")
nome_prod = st.sidebar.text_input("Nome do Produto", "Produto Exemplo")
custo_un = st.sidebar.number_input("Custo Unitário (R$)", min_value=0.01, value=12.05, step=0.01)
frete_forn = st.sidebar.number_input("Frete Fornecedor (%)", min_value=0.0, value=5.0)
imposto = st.sidebar.number_input("Imposto Nota Fiscal (%)", min_value=0.0, value=6.0)
comissao_mkt = st.sidebar.number_input("Comissão Marketplace (%)", min_value=0.0, value=12.0)
preco_venda = st.sidebar.number_input("Preço de Venda Final (R$)", min_value=0.01, value=26.06, step=0.01)

# --- LÓGICA DE CÁLCULO ---
# 1. Custos Fixos e Variáveis
v_frete_forn = custo_un * (frete_forn / 100)
v_imposto = preco_venda * (imposto / 100)
v_comissao = preco_venda * (comissao_mkt / 100)
taxa_fixa = 6.50 if preco_venda < 79.0 else 0.0

custo_total_operacional = custo_un + v_frete_forn + v_imposto + v_comissao + taxa_fixa
lucro_liquido = preco_venda - custo_total_operacional
margem_real_pct = (lucro_liquido / preco_venda) * 100 if preco_venda > 0 else 0

# --- EXIBIÇÃO PRINCIPAL ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Lucro Líquido", f"R$ {lucro_liquido:.2f}")
with col2:
    cor_margem = "normal" if margem_real_pct > 10 else "inverse"
    st.metric("Margem Real (%)", f"{margem_real_pct:.2f}%", delta_color=cor_margem)
with col3:
    st.metric("Custos Totais", f"R$ {custo_total_operacional:.2f}")
with col4:
    st.metric("Taxa Fixa (ML/Shopee)", f"R$ {taxa_fixa:.2f}")

st.divider()

# --- SEÇÃO DE INTELIGÊNCIA DE ADS (ROAS) ---
st.header("🎯 Inteligência de Tráfego (Ads)")

if margem_real_pct > 0:
    # Cálculo do ROAS de Equilíbrio (Break-even)
    roas_equilibrio = 1 / (margem_real_pct / 100)
    
    st.write(f"Para o produto **{nome_prod}**, seu ROAS de equilíbrio é **{roas_equilibrio:.2f}**.")
    
    # Input do ROAS Real que o usuário vê na plataforma (ML/Shopee/Facebook)
    roas_atual = st.slider("Qual o ROAS atual no painel de anúncios?", 
                           min_value=0.0, max_value=20.0, value=float(round(roas_equilibrio + 1, 1)))

    # DIAGNÓSTICO DO ROAS
    if roas_atual < roas_equilibrio:
        st.error(f"🔴 **DIAGNÓSTICO CRÍTICO:** Você está perdendo dinheiro! Seu ROAS ({roas_atual:.1f}) é menor que o necessário ({roas_equilibrio:.2f}). PARE OU AJUSTE IMEDIATAMENTE.")
    elif roas_atual < (roas_equilibrio * 1.2):
        st.warning(f"🟡 **DIAGNÓSTICO: ZONA DE ALERTA.** Você está no 'zero a zero' ou com lucro muito baixo. Bom para ganhar relevância, ruim para o caixa.")
    elif roas_atual < (roas_equilibrio * 2.0):
        st.success(f"🟢 **DIAGNÓSTICO: SAUDÁVEL.** Campanha lucrativa. Você está pagando o Ads e colocando dinheiro no bolso.")
    else:
        st.balloons()
        st.success(f"💎 **DIAGNÓSTICO: ESCALA MÁXIMA.** Este produto é uma estrela! ROAS de {roas_atual:.1f} permite aumentar o orçamento sem medo.")

else:
    st.error("⚠️ **MARGEM NEGATIVA:** Não é possível calcular ROAS para um produto que já dá prejuízo antes mesmo do anúncio. Aumente o preço de venda ou reduza custos.")

# --- TABELA DE RESUMO PARA DOWNLOAD ---
st.divider()
st.subheader("📋 Resumo da Operação")
df_resumo = pd.DataFrame({
    'Produto': [nome_prod],
    'Venda': [preco_venda],
    'Custo Total': [custo_total_operacional],
    'Lucro R$': [lucro_liquido],
    'Margem %': [margem_real_pct],
    'ROAS Min.': [roas_equilibrio if margem_real_pct > 0 else 0]
})
st.table(df_resumo)
