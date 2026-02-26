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
# O uso de value=None faz com que o campo fique vazio até você digitar
st.header("📥 Dados do Produto")
nome_prod = st.text_input("Nome do Produto", placeholder="Ex: Fone Bluetooth")

col1, col2 = st.columns(2)
with col1:
    custo_un = st.number_input("Custo Unitário (R$)", min_value=0.0, step=0.01, value=None, placeholder="0,00")
    imposto = st.number_input("Imposto (%)", min_value=0.0, step=0.1, value=None, placeholder="6.0")
with col2:
    preco_venda = st.number_input("Preço de Venda (R$)", min_value=0.0, step=0.01, value=None, placeholder="0,00")
    comissao = st.number_input("Comissão (%)", min_value=0.0, step=0.1, value=None, placeholder="12.0")

# 3. Lógica de Cálculo (Só executa se os campos forem preenchidos)
if custo_un and preco_venda:
    taxa_fixa = 6.50 if preco_venda < 79 else 0.0
    v_imposto = preco_venda * (imposto / 100) if imposto else 0
    v_comissao = preco_venda * (comissao / 100) if comissao else 0
    
    lucro = preco_venda - custo_un - v_imposto - v_comissao - taxa_fixa
    margem = (lucro / preco_venda) * 100
    
    st.write("---")
    
    # 4. Resultados e Efeito de Estratégia Vencedora
    st.subheader("📊 Resultado Final")
    
    # EFEITO DE ESTRATÉGIA VENCEDORA
    if margem >= 20:
        st.balloons() # Efeito de balões para margens excelentes
        st.success("🏆 **ESTRATÉGIA VENCEDORA DETECTADA!**")
        st.markdown("Este produto possui uma margem de segurança alta e grande potencial de escala.")
    
    st.metric("LUCRO LÍQUIDO", f"R$ {lucro:.2f}")
    st.metric("MARGEM REAL", f"{margem:.2f}%")

    if preco_venda < 79:
        st.warning(f"⚠️ Taxa fixa de R$ 6,50 aplicada (Venda < R$ 79).")

    st.write("---")

    # 5. Meta de Ads (ROAS)
    st.header("🎯 Meta de Ads (ROAS)")
    if margem > 0:
        roas_eb = 1 / (margem / 100)
        st.info(f"Seu ROAS de Equilíbrio é: **{roas_eb:.2f}**")
        
        roas_atual = st.slider("Quanto está o ROAS no painel?", 0.0, 20.0, float(round(roas_eb + 1, 1)))
        
        if roas_atual < roas_eb:
            st.error(f"🔴 PREJUÍZO! O ROAS está abaixo do ponto de equilíbrio.")
        elif roas_atual < (roas_eb * 1.5):
            st.warning("🟡 ALERTA: Operação saudável, mas com pouco lucro real.")
        else:
            st.success("🟢 EXCELENTE: Campanha gerando lucro líquido real!")
    else:
        st.error("❌ Margem negativa. Ajuste os custos ou preço antes de anunciar.")

else:
    st.info("💡 Preencha o Custo e o Preço de Venda para ver a análise.")
