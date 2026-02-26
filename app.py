import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Omni Stratagem", page_icon="🎯")

# Estilo para destacar os botões
st.markdown("""
    <style>
    .stButton>button { 
        width: 100%; border-radius: 8px; height: 3em; 
        background-color: #1E3A8A; color: white; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Omni Stratagem")
st.markdown('**Soluções inteligentes para o seu Ecommerce.**')

# --- ENTRADA DE DADOS ---
nome_prod = st.text_input("Produto", placeholder="Ex: Fone Bluetooth")

col1, col2 = st.columns(2)
with col1:
    custo = st.number_input("Custo (R$)", min_value=0.0, value=None, placeholder="0.00")
with col2:
    venda = st.number_input("Venda (R$)", min_value=0.0, value=None, placeholder="0.00")

# --- PARÂMETROS ---
with st.expander("🛠️ Parâmetros Estratégicos"):
    taxa_imposto = st.slider("Imposto (%)", 0, 30, 6)
    taxa_mkt = st.slider("Taxa Marketplace (%)", 0, 30, 12)
    
    # Seleção de Taxas por Canal
    opcoes_taxa = {
        "Sem Taxa Fixa": 0.0,
        "R$ 4,00 (Destaque Shopee)": 4.0,
        "R$ 6,25 (Mercado Livre)": 6.25,
        "R$ 6,50 (Mercado Livre)": 6.50,
        "R$ 6,75 (Mercado Livre)": 6.75
    }
    selecao_taxa = st.selectbox("Canal de Venda (Taxa Fixa):", list(opcoes_taxa.keys()))
    valor_fixa = opcoes_taxa[selecao_taxa]

# --- BOTÃO E CÁLCULOS ---
if st.button("ANALISAR VIABILIDADE"):
    if custo is None or venda is None:
        st.warning("⚠️ Preencha os valores de custo e venda.")
    else:
        # Lógica matemática
        v_imp = venda * (taxa_imposto / 100)
        v_mkt = venda * (taxa_mkt / 100)
        lucro = venda - (custo + v_imp + v_mkt + valor_fixa)
        
        st.divider()
        if lucro > 0:
            st.toast('🚀 Estratégia vencedora!', icon='✅')
            st.success(f"**LUCRO LÍQUIDO:** R$ {lucro:.2f}")
            
            # Gráfico de Pizza
            dados = {
                "Categoria": ["Custo", "Impostos", "Taxas/Canal", "Lucro"],
                "Valores": [custo, v_imp, v_mkt + valor_fixa, lucro]
            }
            fig = px.pie(dados, values='Valores', names='Categoria', hole=.3)
            st.plotly_chart(fig)
        else:
            st.error(f"**ALERTA DE PREJUÍZO:** R$ {lucro:.2f}")
            st.warning("Sugestão Omni: Revise o preço de venda ou negocie o custo.")
