import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração de Página (Layout Centralizado para Mobile)
st.set_page_config(
    page_title="Smart Commerce Pro", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- CSS PARA MOBILE (Cards Flexíveis) ---
st.markdown("""
    <style>
    .metric-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        text-align: center;
        border: 1px solid #f0f2f6;
        margin-bottom: 10px;
    }
    .metric-title { font-size: 12px; color: #6b7280; font-weight: 600; }
    .metric-value { font-size: 20px; color: #1e293b; font-weight: 700; }
    .metric-icon { font-size: 24px; }
    
    /* Ajuste para inputs no mobile */
    .stNumberInput { margin-bottom: -10px; }
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO ---
st.title("🚀 Smart Commerce")
st.caption("Omni Stratagem LTDA | Gestão Mobile")

# --- ETAPA 1: CUSTOS FIXOS (EM EXPANDER PARA ECONOMIZAR TELA) ---
with st.expander("🛠️ Configurar Custos Base (Imposto/Comissão)", expanded=False):
    custo_un = st.number_input("Custo Unitário (R$)", min_value=0.0, step=0.01, value=None, placeholder="0,00")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        imposto = st.number_input("Imposto (%)", min_value=0.0, step=0.1, value=6.0)
    with col_c2:
        comissao = st.number_input("Comissão (%)", min_value=0.0, step=0.1, value=12.0)

st.write("---")

# --- ETAPA 2: PRECIFICAÇÃO (O QUE MUDA TODA HORA) ---
st.subheader("💰 Simulação de Venda")
nome_prod = st.text_input("Nome do Produto", placeholder="Ex: Smartwatch")
preco_venda = st.number_input("Preço de Venda Final (R$)", min_value=0.0, step=0.01, value=None, placeholder="0,00")

# Lógica de Automação de Faixa (Oculta para o usuário não perder tempo)
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

# Peso em destaque pois influi muito no frete
sel_peso = st.selectbox("Qual o Peso?", ["Até 0,3 kg", "De 0,3 a 0,5 kg", "De 0,5 a 1 kg", "De 1 a 1,5 kg", "De 1,5 a 2 kg", "De 2 a 3 kg", "De 3 a 4 kg", "De 4 a 5 kg", "De 5 a 6 kg", "De 9 a 11 kg", "De 20 a 25 kg", "De 70 a 80 kg"])

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
frete_val = tabela_frete[sel_peso][idx_auto]

# --- ETAPA 3: RESULTADOS (EM CARDS PARA CELULAR) ---
if preco_venda and custo_un:
    st.write("---")
    v_imp = preco_venda * (imposto / 100)
    v_com = preco_venda * (comissao / 100)
    lucro = preco_venda - custo_un - v_imp - v_com - frete_val
    margem = (lucro / preco_venda) * 100

    # Layout Vertical de Cards (Melhor para o dedo no celular)
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">💵</div>
            <div class="metric-title">LUCRO LÍQUIDO</div>
            <div class="metric-value">R$ {lucro:.2f}</div>
        </div>
        <div class="metric-card">
            <div class="metric-icon">📈</div>
            <div class="metric-title">MARGEM REAL</div>
            <div class="metric-value">{margem:.1f}%</div>
        </div>
        <div class="metric-card">
            <div class="metric-icon">🚚</div>
            <div class="metric-title">CUSTO FRETE (Auto)</div>
            <div class="metric-value">R$ {frete_val:.2f}</div>
        </div>
    """, unsafe_allow_html=True)

    if margem >= 20:
        st.success("🚀 ESTRATÉGIA VENCEDORA!")
        st.toast("Sucesso!", icon="🚀")

    # Gráfico Donut (Ajustado para tela pequena)
    df_p = pd.DataFrame({
        "Cat": ["Prod", "Imp", "Com", "Fr", "Luc"],
        "Val": [custo_un, v_imp, v_com, frete_val, max(0, lucro)]
    })
    fig = px.pie(df_p, values='Val', names='Cat', hole=0.5, color_discrete_sequence=px.colors.qualitative.Bold)
    fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=250, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

    # --- ETAPA 4: ADS (ROAS) ---
    st.write("---")
    st.subheader("
