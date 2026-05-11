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
# FUNÇÃO DE FORMATAÇÃO
# ======================================

def formatar_moeda(valor):

    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ======================================
# TÍTULO
# ======================================

st.title("💰 Preço Certo")

st.caption(
    "Precifique com inteligência."
)

st.divider()

# ======================================
# LAYOUT PRINCIPAL
# ======================================

col1, col2 = st.columns([1, 1])

# ======================================
# COLUNA ESQUERDA
# ======================================

with col1:

    st.subheader("📦 Dados do Produto")

    nome_produto = st.text_input(
        "Nome do Produto ou Serviço",
        help="Digite o nome do produto ou serviço que será precificado."
    )

    st.divider()

    # ==================================
    # CUSTOS DIRETOS
    # ==================================

    st.subheader("💵 Custos Diretos (R$)")

    custo_produto = st.number_input(
        "Produto / Material",
        min_value=0.0,
        format="%.2f",
        help="Valor pago pelo produto ou matéria-prima."
    )

    frete = st.number_input(
        "Frete / Deslocamento",
        min_value=0.0,
        format="%.2f",
        help="Custos de entrega, transporte ou deslocamento."
    )

    outros_custos = st.number_input(
        "Outros Custos",
        min_value=0.0,
        format="%.2f",
        help="Custos adicionais relacionados à operação."
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
        format="%.2f",
        help="Percentual de impostos cobrados sobre a venda."
    )

    taxas = st.number_input(
        "Taxas (%)",
        min_value=0.0,
        max_value=100.0,
        format="%.2f",
        help="Taxas de cartão, marketplace ou gateway."
    )

    comissao = st.number_input(
        "Comissão (%)",
        min_value=0.0,
        max_value=100.0,
        format="%.2f",
        help="Percentual pago em comissão sobre a venda."
    )

    administrativo = st.number_input(
        "Custo Administrativo (%)",
        min_value=0.0,
        max_value=100.0,
        format="%.2f",
        help="Custos indiretos do negócio (energia, aluguel, internet, etc)."
    )

    perdas = st.number_input(
        "Perdas (%)",
        min_value=0.0,
        max_value=100.0,
        format="%.2f",
        help="Margem para desperdícios, trocas ou imprevistos."
    )

    st.divider()

    # ==================================
    # OBJETIVO DE LUCRO
    # ==================================

    st.subheader("🎯 Objetivo de Lucro")

    margem = st.slider(
        "Margem Desejada (%)",
        min_value=0,
        max_value=100,
        value=30,
        help="Percentual de lucro desejado sobre a venda."
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

            # ==================================
            # ALERTAS INTELIGENTES
            # ==================================

            if resultado['percentual_operacional'] > 40:

                st.warning(
                    "⚠️ Seus custos operacionais estão altos. Isso pode reduzir sua competitividade."
                )

            if resultado['markup'] > 4:

                st.warning(
                    "⚠️ O markup está elevado. Verifique se o preço continua competitivo."
                )

            if resultado['margem_real'] < 10:

                st.warning(
                    "⚠️ Sua margem de lucro está baixa."
                )

            if resultado['margem_real'] >= 30:

                st.success(
                    "✅ Sua margem está saudável."
                )

            # ==============================
            # CARDS
            # ==============================

            c1, c2 = st.columns(2)

            with c1:

                st.metric(
                    "💵 Custos Diretos",
                    formatar_moeda(resultado['custos_diretos'])
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
                    formatar_moeda(resultado['preco_sugerido'])
                )

                st.metric(
                    "💰 Lucro Líquido",
                    formatar_moeda(resultado['lucro'])
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

            grafico.update_traces(
                textposition='inside',
                textinfo='percent+label'
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

            breakdown_exibicao = breakdown.copy()

            breakdown_exibicao["Valor"] = breakdown_exibicao["Valor"].apply(
                formatar_moeda
            )

            st.dataframe(
                breakdown_exibicao,
                use_container_width=True
            )

            st.divider()

            # ==============================
            # DIAGNÓSTICO FINANCEIRO
            # ==============================

            st.subheader("🧾 Diagnóstico Financeiro")

            st.info(f"""

Produto/Serviço: {nome_produto}

💵 Custos Diretos:
{formatar_moeda(resultado['custos_diretos'])}

📊 Custos Operacionais:
{resultado['percentual_operacional']}%

⚙️ Markup Equivalente:
{resultado['markup']}x

📈 Margem Real:
{resultado['margem_real']}%

💰 Lucro Líquido:
{formatar_moeda(resultado['lucro'])}

🏷️ Preço Final Sugerido:
{formatar_moeda(resultado['preco_sugerido'])}

""")