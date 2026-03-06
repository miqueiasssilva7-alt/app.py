import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração de Página Pro
st.set_page_config(
    page_title="Smart Commerce Pro", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- CSS PARA ESTILIZAÇÃO DOS CARDS E ÍCONES ---
st.markdown("""
    <style>
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        text-align: center;
        border: 1px solid #f0f2f6;
    }
    .metric-title { font-size: 14px; color: #6b7280; font-weight: 600; margin-bottom: 5px; }
    .metric-value { font-size: 24px; color: #1e293b; font-weight: 700; }
    .metric-icon { font-size: 28px; margin-bottom: 10px; }
    
    /* Estilo da Sidebar */
    [data-testid="stSidebar"] { background-color: #f8fafc; border-right: 1px solid #e2e8f0; }
    </style>
    """, unsafe_allow_html=True)

# --- MENU LATERAL (CONFIGURAÇÕES) ---
with st.sidebar:
    st.markdown("## ⚙️ Configurações")
    st.caption("Ajuste os custos operacionais")
    
    # value=None faz com que o campo venha vazio, sem o 0.0 travado
    custo_un = st.number_input("Custo Unitário (R$)", min_value=0.0, step=0.01, value=None, placeholder="0,00")
    imposto = st.number_input("Imposto (%)", min_value=0.0, step=0.1, value=None, placeholder="6.0")
    comissao = st.number_input("Comissão (%)", min_value=0.0, step=0.1, value=None, placeholder="12.0")
    
    st.write("---")
    st.markdown("### 🏷️ Produto")
    nome_prod = st.text_input("Nome do Produto", placeholder="Ex: Smartwatch Ultra")
    
    st.write("---")
    st.caption("🚀 Omni Stratagem LTDA v2.1")

# --- ÁREA PRINCIPAL ---
st.title("🚀 Smart Commerce Pro")
st.write("---")

col_input, col_viz = st.columns([1, 1.2], gap="large")

with col_input:
    st.subheader("💰 Precificação e Frete")
    # Novamente value=None para facilitar a digitação
    preco_venda = st.number_input("Preço de Venda Final (R$)", min_value=0.0, step=0.01, value=None, placeholder="0,00")

    # Lógica de Automação de Faixa (Sempre ativa)
    idx_auto = 0
    pv = preco_venda if preco_venda else 0
    if pv <= 18.99: idx_auto = 0
    elif pv <= 48.99: idx_auto = 1
    elif pv <= 78.99: idx_auto = 2
    elif pv <= 99.99: idx_auto = 3
    elif pv <= 119.99: idx_auto = 4
    elif pv <= 149.99: idx_auto = 5
    elif pv <= 199.99: idx_auto = 6
    else: idx_auto = 7

    faixas_venda = ["R$ 0-18", "R$ 19-48", "R$ 49-78", "R$ 79-99", "R$ 100-119", "R$ 120-149", "R$ 150-199", "R$ 200+"]
    sel_faixa_venda = st.selectbox("Faixa de Venda (Auto):", faixas_venda, index=idx_auto)
    
    tabela_frete = {
        "Até 0,3 kg": [5.65, 6.55, 7.75, 12.35, 14.35, 16.45, 18.45, 20.95],
        "De 0,3 a 0,5 kg": [5.95, 6.65, 7.85, 13.25, 15.45, 17.65, 19.85, 22.55],
        "De 0,5 a 1 kg": [6.05, 6.75, 7.95, 13.85, 16.15, 18.45, 20.75, 23.65],
        "De 1 a 1,5 kg": [6.15, 6.85, 8.05, 14.15, 16.45, 18.85, 21.15, 24.65],
        "De 1,5 a 2 kg": [6.25, 6.95, 8.15, 14.45, 16.85, 19.25, 21.65, 24.65],
        "De 2 a 3 kg": [6.35, 7.95, 8.55, 15.75, 18.35, 21.05, 23.65, 26.25],
        "De 3 a 4 kg": [6.45, 8.15, 8.95, 17.05, 19.85, 22.65, 25.55, 28.35],
        "De 4 a 5 kg": [6.55, 8.35, 9.75, 18.45, 21.55, 24.65, 27.75, 30
