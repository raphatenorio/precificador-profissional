import streamlit as st
import plotly.express as px
import pandas as pd

from calculos import calcular_preco

# ======================================
# CONFIGURAÇÃO DA PÁGINA
# ======================================

st.set_page_config(

    page_title="Preço Certo",
    layout="wide"

)

# ======================================
# TÍTULO
# ======================================

st.title("💰 Preço Certo")

st.caption(
    "Sistema profissional de precificação"
)

st.divider()

# ======================================
# LAYOUT
# ======================================

col1, col2 = st.columns([1, 1])

# ======================================
# COLUNA ESQUERDA
# ======================================

with col1:

    st.subheader("📦 Dados do Produto")

    nome_produto = st.text_input(
        "Nome do Produto ou Serviço"
    )

    st.divider()

    # ==================================
    # CUSTOS DIRETOS
    # ==================================

    st.subheader("💵 Custos Diretos (R$)")

    custo_produto = st.number_input(
        "Produto / Material",
        min_value=0.0,
        format="%.2f"
    )

    frete = st.number_input(
        "Frete / Deslocamento",
        min_value=0.0,
        format="%.2f"
    )

    outros_custos = st.number_input(
        "Outros Custos",
        min_value=0.0,
        format="%.2f"
    )

    st.divider()

    # ==================================
    # CUSTOS OPERACIONAIS
    # ==================================

    st.subheader("📊 Custos Operacionais (%)")

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

    administrativo = st.number_input(
        "Custo Administrativo (%)",
        min_value=0.0,
        max_value=100.0,
        format="%.2f"
    )

    perdas = st.number_input(
        "Perdas (%)",
        min_value=0.0,
        max_value=100.0,
        format="%.2f"
    )

    st.divider()

    # ==================================
    # MARGEM
    # ==================================

    st.subheader("🎯 Objetivo de Lucro")

    margem = st.slider(
        "Margem Desejada (%)",
        min_value=0,
        max_value=100,
        value=30
    )

    st.divider()

    calcular = st.button(
        "🚀 Calcular Preço",
        use_container_width=True
    )

# ======================================
# COLUNA DIREITA
# ======================================

with col2:

    st.subheader("📈 Dashboard Financeiro")

    if calcular:

        resultado = calcular_preco(

            custo_produto,
            frete,
            outros_custos,

            impostos,
            taxas,
            comissao,
            administrativo,
            perdas,

            margem

        )

        # ==================================
        # ERRO
        # ==================================

        if "erro" in resultado:

            st.error(resultado["erro"])

        else:

            # ==============================
            # CARDS
            # ==============================

            c1, c2 = st.columns(2)

            with c1:

                st.metric(
                    "💵 Custos Diretos",
                    f"R$ {resultado['custos_diretos']}"
                )

                st.metric(
                    "📊 Custos Operacionais",
                    f"{resultado['percentual_operacional']}%"
                )

                st.metric(
                    "📈 Margem Real",
                    f"{resultado['margem_real']}%"
                )

            with c2:

                st.metric(
                    "🏷️ Preço Sugerido",
                    f"R$ {resultado['preco_sugerido']}"
                )

                st.metric(
                    "💰 Lucro Líquido",
                    f"R$ {resultado['lucro']}"
                )

                st.metric(
                    "⚙️ Markup Equivalente",
                    f"{resultado['markup']}x"
                )

            st.divider()

            # ==============================
            # BREAKDOWN
            # ==============================

            st.subheader("🔍 Breakdown Financeiro")

            breakdown = pd.DataFrame({

                "Categoria": [

                    "Custos Diretos",
                    "Impostos",
                    "Taxas",
                    "Comissão",
                    "Administrativo",
                    "Perdas",
                    "Lucro"

                ],

                "Valor": [

                    resultado['custos_diretos'],
                    resultado['valor_impostos'],
                    resultado['valor_taxas'],
                    resultado['valor_comissao'],
                    resultado['valor_administrativo'],
                    resultado['valor_perdas'],
                    resultado['lucro']

                ]
            })

            grafico = px.pie(

                breakdown,

                names="Categoria",
                values="Valor",
                hole=0.5

            )

            st.plotly_chart(
                grafico,
                use_container_width=True
            )

            st.divider()

            # ==============================
            # TABELA
            # ==============================

            st.subheader("📋 Composição do Preço")

            st.dataframe(
                breakdown,
                use_container_width=True
            )

            st.divider()

            # ==============================
            # RESUMO
            # ==============================

            st.subheader("🧾 Resumo Executivo")

            st.info(f"""

            Produto/Serviço: {nome_produto}

            Custos Diretos: R$ {resultado['custos_diretos']}

            Custos Operacionais: {resultado['percentual_operacional']}%

            Markup Equivalente: {resultado['markup']}x

            Margem Real: {resultado['margem_real']}%

            Lucro Líquido: R$ {resultado['lucro']}

            Preço Final Sugerido: R$ {resultado['preco_sugerido']}

            """)