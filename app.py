import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Omni Stratagem", page_icon="🎯")

st.title("🛡️ Omni Stratagem")
st.markdown('**Soluções inteligentes para o seu negócio.**')

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
    
    # Criamos a variável segura aqui, logo após 'venda' ser definida
    v_segura = venda if venda is not None else 0.0
    tem_taxa_fixa = st.checkbox("Taxa Fixa (R$ 6,50)", value=(v_segura < 79 and v_segura > 0))

# --- BOTÃO E CÁLCULOS ---
if st.button("ANALISAR VIABILIDADE"):
    if custo is None or venda is None:
        st.warning("⚠️ Preencha os valores de custo e venda.")
    else:
        # Lógica matemática
        valor_imposto = venda * (taxa_imposto / 100)
        valor_mkt = venda * (taxa_mkt / 100)
        valor_fixa = 6.50 if tem_taxa_fixa else 0
        lucro = venda - (custo + valor_imposto + valor_mkt + valor_fixa)
        
        st.divider()
        if lucro > 0:
            st.success(f"**LUCRO LÍQUIDO:** R$ {lucro:.2f}")
            
            # Gráfico de Pizza
            dados = {
                "Categoria": ["Custo", "Impostos", "Taxas", "Lucro"],
                "Valores": [custo, valor_imposto, valor_mkt + valor_fixa, lucro]
            }
            fig = px.pie(dados, values='Valores', names='Categoria', hole=.3)
            st.plotly_chart(fig)
        else:
            st.error(f"**PREJUÍZO:** R$ {lucro:.2f}")
