import streamlit as st

from calculos import calcular_preco

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================

st.set_page_config(
    page_title="Preço Certo",
    layout="centered"
)

# =========================
# TÍTULO
# =========================

st.title("💰 Preço Certo")

st.write("Sistema profissional de precificação")

st.divider()

# =========================
# NOME DO PRODUTO
# =========================

nome_produto = st.text_input(
    "Nome do Produto ou Serviço"
)

# =========================
# CUSTOS FIXOS
# =========================

st.subheader("Custos Fixos (R$)")

custo_produto = st.number_input(
    "Custo do Produto",
    min_value=0.0,
    format="%.2f"
)

frete = st.number_input(
    "Frete",
    min_value=0.0,
    format="%.2f"
)

outros_custos = st.number_input(
    "Outros Custos",
    min_value=0.0,
    format="%.2f"
)

st.divider()

# =========================
# PERCENTUAIS
# =========================

st.subheader("Percentuais (%)")

impostos = st.number_input(
    "Impostos (%)",
    min_value=0.0,
    max_value=100.0,
    format="%.2f"
)

taxas = st.number_input(
    "Taxas (%)",
    min_value=0.0,
    max_value=100.0,
    format="%.2f"
)

comissao = st.number_input(
    "Comissão (%)",
    min_value=0.0,
    max_value=100.0,
    format="%.2f"
)

margem = st.slider(
    "Margem de Lucro (%)",
    min_value=0,
    max_value=100,
    value=30
)

st.divider()

# =========================
# BOTÃO
# =========================

if st.button("Calcular Preço"):

    resultado = calcular_preco(
        custo_produto,
        frete,
        outros_custos,
        impostos,
        taxas,
        comissao,
        margem
    )

    # Verifica erro
    if "erro" in resultado:
        st.error(resultado["erro"])

    else:

        st.success("Precificação realizada com sucesso!")

        st.subheader("Resultado")

        st.metric(
            "Custos Fixos",
            f"R$ {resultado['custos_fixos']}"
        )

        st.metric(
            "Percentuais Totais",
            f"{resultado['percentual_total']}%"
        )

        st.metric(
            "Lucro Esperado",
            f"R$ {resultado['lucro']}"
        )

        st.metric(
            "Preço Sugerido",
            f"R$ {resultado['preco_sugerido']}"
        )