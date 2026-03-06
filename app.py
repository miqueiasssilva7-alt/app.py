import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração de Página Pro
st.set_page_config(
    page_title="Smart Commerce Pro", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- CSS PERSONALIZADO PARA LOOK DE APP ---
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 1.8rem !important; color: #1E88E5; }
    [data-testid="stSidebar"] { background-color: #f1f3f6; }
    .main { background-color: #ffffff; }
    div.stButton > button:first-child { background-color: #00c853; color: white; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- MENU LATERAL (CONFIGURAÇÕES) ---
with st.sidebar:
    st.title("⚙️ Painel de Custos")
    st.write("Ajuste os valores base aqui:")
    
    custo_un = st.number_input("💰 Custo Unitário (R$)", min_value=0.0, step=0.01, value=0.0)
    imposto = st.number_input("🏦 Imposto (%)", min_value=0.0, step=0.1, value=6.0)
    comissao = st.number_input("🧧 Comissão (%)", min_value=0.0, step=0.1, value=12.0)
    
    st.write("---")
    st.caption("🚀 Omni Stratagem LTDA | 2026")
    st.caption("Versão 2.0 - Interface Pro")

# --- ÁREA PRINCIPAL ---
st.title("🚀 Smart Commerce Pro")
st.markdown("##### Inteligência em Lucratividade e Ads")
st.write("---")

# Layout em Colunas (Esquerda: Entradas | Direita: Resultados)
col_input, col_viz = st.columns([1, 1.2], gap="large")

with col_input:
    st.subheader("🏷️ Precificação")
    nome_prod = st.text_input("Nome do Produto", placeholder="Ex: Smartwatch Ultra")
    preco_venda = st.number_input("Preço de Venda Final (R$)", min_value=0.0, step=0.01, value=0.0)

    # Lógica de Automação de Faixa de Preço
    faixas_venda = [
        "R$ 0 a R$ 18,99", "R$ 19 a R$ 48,99", "R$ 49 a R$ 78,99", "R$ 79 a R$ 99,99", 
        "R$ 100 a R$ 119,99", "R$ 120 a R$ 149,99", "R$ 150 a R$ 199,99", "A partir de R$ 200"
    ]
    
    idx_auto = 0
    if preco_venda <= 18.99: idx_auto = 0
    elif preco_venda <= 48.99: idx_auto = 1
    elif preco_venda <= 78.99: idx_auto = 2
    elif preco_venda <= 99.99: idx_auto = 3
    elif preco_venda <= 119.99: idx_auto = 4
    elif preco_venda <= 149.99: idx_auto = 5
    elif preco_venda <= 199.99: idx_auto = 6
    else: idx_auto = 7

    st.write("🚚 **Logística de Frete**")
    sel_faixa_venda = st.selectbox("Faixa de Venda (Identificada):", faixas_venda, index=idx_auto)
    
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
    
    sel_peso = st.selectbox("Peso do Produto:", list(tabela_frete.keys()))
    frete_val = tabela_frete[sel_peso][faixas_venda.index(sel_faixa_venda)]

with col_viz:
    if preco_venda > 0 and custo_un > 0:
        v_imposto = preco_venda * (imposto / 100)
        v_comissao = preco_venda * (comissao / 100)
        lucro = preco_venda - custo_un - v_imposto - v_comissao - frete_val
        margem = (lucro / preco_venda) * 100 if preco_venda > 0 else 0

        st.subheader("📊 Resultados")
        
        # Métricas em Cards
        m1, m2, m3 = st.columns(3)
        m1.metric("Lucro Líquido", f"R$ {lucro:.2f}")
        m2.metric("Margem Real", f"{margem:.1f}%")
        m3.metric("Custo Frete", f"R$ {frete_val:.2f}")

        if margem >= 20:
            st.success("🚀 **ESTRATÉGIA VENCEDORA!**")
            st.toast("Produto Campeão!", icon="🚀")

        # Gráfico Donut Moderno
        dados_grafico = {
            "Categoria": ["Custo", "Imposto", "Comissão", "Frete", "Lucro"],
            "Valores": [custo_un, v_imposto, v_comissao, frete_val, max(0, lucro)]
        }
        df_pizza = pd.DataFrame(dados_grafico)
        fig = px.pie(df_pizza, values='Valores', names='Categoria', hole=0.5,
                     color_discrete_sequence=px.colors.sequential.RdBu)
        fig.update_layout(margin=dict(t=30, b=0, l=0, r=0), height=350, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("👋 Preencha os dados à esquerda para gerar a análise em tempo real.")

# --- SEÇÃO DE ADS (ROAS) ---
if preco_venda > 0 and margem > 0:
    st.write("---")
    st.header("🎯 Meta de Ads (ROAS)")
    
    roas_eb = 1 / (margem / 100)
    
    col_roas1, col_roas2 = st.columns([1, 2])
    with col_roas1:
        st.metric("ROAS de Equilíbrio", f"{roas_eb:.2f}")
        st.caption("Abaixo disso, a operação perde dinheiro.")
    
    with col_roas2:
        roas_atual = st.slider("Ajuste para simular seu ROAS atual:", 0.1, 20.0, float(round(roas_eb + 1, 1)))
        if roas_atual < roas_eb:
            st.error(f"🔴 Atenção: Com ROAS {roas_atual}, você está no prejuízo.")
        else:
            lucro_final_ads = (1 - (roas_eb / roas_atual)) * margem
            st.success(f"🟢 Lucrativo! Margem final após Ads: {lucro_final_ads:.2f}%")
