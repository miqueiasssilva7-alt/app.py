import streamlit as st
import pandas as pd

# Configurações iniciais da página
st.set_page_config(page_title="SmartCommerce AI", page_icon="🛒", layout="centered")

# Estilo CSS para deixar com cara de App de Celular
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { 
        width: 100%; 
        border-radius: 8px; 
        height: 3.5em; 
        background-color: #1E3A8A; 
        color: white;
        font-weight: bold;
    }
    .welcome-text {
        font-size: 1.1em;
        color: #4B5563;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Omni Stratagem")
st.caption("A inteligência por trás do seu lucro")

# Menu de navegação superior
aba1, aba2 = st.tabs(["⚖️ Calculadora", "📦 Meu Estoque"])

with aba1:
    st.write("### Simular Venda")
    
    with st.container():
        nome = st.text_input("Nome do Produto", placeholder="Ex: Fone Bluetooth")
        col1, col2 = st.columns(2)
        with col1:
            custo = st.number_input("Custo (R$)", min_value=0.0, format="%.2f", value=None, placeholder="0,00")
        with col2:
            venda = st.number_input("Venda (R$)", min_value=0.0, format="%.2f", value=None, placeholder="0,00")
            
    # Configurações de taxas (podemos automatizar depois)
    with st.expander("🛠️ Parâmetros Estratégicos"):
        taxa_imposto = st.slider("Alíquota de Imposto (%)", 0, 30, 6)
        taxa_mkt = st.slider("Taxa do Marketplace (%)", 0, 30, 12)
        
        # Proteção contra erro: se preco_venda for None, usamos 0.0
        venda_segura = preco_venda if preco_venda is not None else 0.0
        
        tem_taxa_fixa = st.checkbox("Aplicar Taxa Fixa (R$ 6,50)", value=(venda_segura < 79 and venda_segura > 0))
    if st.button("CALCULAR DIAGNÓSTICO"):
        # Lógica de cálculo
        v_imposto = venda * (imposto/100)
        v_comissao = venda * (comissao/100)
        v_taxa = 6.50 if frete_fixo else 0
        
        total_custos = custo + v_imposto + v_comissao + v_taxa
        lucro = venda - total_custos
        margem = (lucro / venda * 100) if venda > 0 else 0
        
        st.divider()
        if lucro > 0:
            st.toast('🚀 Estratégia vencedora!', icon='✅')
            st.success(f"**LUCRO LÍQUIDO:** R$ {lucro:.2f}")
            st.info(f"**MARGEM REAL:** {margem:.2f}%")
        else:
            st.error(f"**PREJUÍZO DETECTADO:** R$ {lucro:.2f}")
            st.warning("Dica: Considere criar um kit ou aumentar o preço.")

with aba2:
    st.write("### Gestão de Inventário")
    st.warning("Estamos conectando o banco de dados seguro... Em breve você poderá salvar seus produtos aqui!")
