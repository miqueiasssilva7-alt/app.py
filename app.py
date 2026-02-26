import streamlit as st
import pandas as pd

# 1. Configuração de Página
st.set_page_config(page_title="Smart Commerce", layout="centered")

# --- CABEÇALHO PERSONALIZADO ---
st.title("🚀 Smart Commerce")
st.markdown("### Omni Stratagem LTDA")
st.caption("Gestão de Lucro e Meta de Ads")
st.write("---")

# 2. Entrada de Dados
st.header("📥 Dados do Produto")
nome_prod = st.text_input("Nome do Produto", placeholder="Ex: Fone Bluetooth")

col1, col2 = st.columns(2)
with col1:
    custo_un = st.number_input("Custo Unitário (R$)", min_value=0.0, step=0.01, value=None, placeholder="0,00")
    imposto = st.number_input("Imposto (%)", min_value=0.0, step=0.1, value=None, placeholder="6.0")
with col2:
    preco_venda = st.number_input("Preço de Venda (R$)", min_value=0.0, step=0.01, value=None, placeholder="0,00")
    comissao = st.number_input("Comissão (%)", min_value=0.0, step=0.1, value=None, placeholder="12.0")

# --- NOVA SEÇÃO DE TAXA FIXA SELECIONÁVEL ---
st.write("---")
st.subheader("📌 Regra de Taxa Fixa")

# Criamos as opções de taxas para o usuário escolher
opcoes_taxas = {
    "Nenhuma (Venda > R$ 79 ou Isento)": 0.0,
    "ML: Taxa Fixa R$ 6,25": 6.25,
    "ML: Taxa Fixa R$ 6,50": 6.50,
    "ML: Taxa Fixa R$ 6,75": 6.75,
    "Shopee: Taxa Fixa R$ 4,00": 4.00,
    "Shopee: Taxa Fixa R$ 18,00": 18.00,
    "Shopee: Taxa Fixa R$ 26,00": 26.00
}

escolha_taxa = st.selectbox(
    "Selecione a Taxa Fixa aplicada a este produto:",
    options=list(opcoes_taxas.keys())
)
taxa_fixa_selecionada = opcoes_taxas[escolha_taxa]

# 3. Lógica de Cálculo
if custo_un and preco_venda:
    v_imposto = preco_venda * (imposto / 100) if imposto else 0
    v_comissao = preco_venda * (comissao / 100) if comissao else 0
    
    # Cálculo final usando a taxa escolhida pelo usuário
    lucro = preco_venda - custo_un - v_imposto - v_comissao - taxa_fixa_selecionada
    margem = (lucro / preco_venda) * 100 if preco_venda > 0 else 0
    
    st.write("---")
    
    # 4. Resultados e Efeito de Estratégia Vencedora
    st.subheader("📊 Resultado Final")
    
    if margem >= 20:
        st.balloons()
        st.success("🏆 **ESTRATÉGIA VENCEDORA DETECTADA!**")
        st.markdown(f"Este produto no **{escolha_taxa.split(':')[0]}** possui excelente potencial.")
    
    col_res1, col_res2 = st.columns(2)
    col_res1.metric("LUCRO LÍQUIDO", f"R$ {lucro:.2f}")
    col_res2.metric("MARGEM REAL", f"{margem:.2f}%")

    st.info(f"Taxa Fixa aplicada: R$ {taxa_fixa_selecionada:.2f}")

    st.write("---")

    # 5. Meta de Ads (ROAS)
    st.header("🎯 Meta de Ads (ROAS)")
    if margem > 0:
        roas_eb = 1 / (margem / 100)
        st.info(f"Seu ROAS de Equilíbrio é: **{roas_eb:.2f}**")
        
        roas_atual = st.slider("Quanto está o ROAS no painel?", 0.0, 20.0, float(round(roas_eb + 1, 1)))
        
        if roas_atual < roas_eb:
            st.error(f"🔴 PREJUÍZO! ROAS abaixo de {roas_eb:.2f}")
        elif roas_atual < (roas_eb * 1.5):
            st.warning("🟡 ALERTA: Operação saudável, lucro estreito.")
        else:
            st.success("🟢 EXCELENTE: Lucro líquido real garantido!")
    else:
        st.error("❌ Margem negativa. Ajuste os custos antes de anunciar.")

else:
    st.info("💡 Preencha os dados acima para calcular.")
