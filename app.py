import streamlit as st
import plotly.express as px
import pandas as pd

from calculos import calcular_preco

from auth import (
    cadastrar_usuario,
    login_usuario,
    logout_usuario
)

# ======================================
# CONFIGURAÇÃO DA PÁGINA
# ======================================

st.set_page_config(

    page_title="Preço Certo",
    layout="wide"

)

# ======================================
# CONTROLE DE SESSÃO
# ======================================

if "usuario" not in st.session_state:

    st.session_state.usuario = None

# ======================================
# FUNÇÃO DE FORMATAÇÃO
# ======================================

def formatar_moeda(valor):

    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ======================================
# AUTENTICAÇÃO
# ======================================

if not st.session_state.usuario:

    st.title("🔐 Login")

    st.caption(
        "Entre ou crie sua conta para acessar o Preço Certo."
    )

    st.divider()

    aba_login, aba_cadastro = st.tabs([
        "Entrar",
        "Cadastrar"
    ])

    # ==================================
    # LOGIN
    # ==================================

    with aba_login:

        st.subheader("Acessar Conta")

        email_login = st.text_input(
            "Email",
            key="login_email"
        )

        senha_login = st.text_input(
            "Senha",
            type="password",
            key="login_senha"
        )

        if st.button(
            "Entrar",
            use_container_width=True
        ):

            resposta = login_usuario(
                email_login,
                senha_login
            )

            if resposta and resposta.user:

                st.session_state.usuario = resposta.user

                st.success(
                    "✅ Login realizado com sucesso!"
                )

                st.rerun()

    # ==================================
    # CADASTRO
    # ==================================

    with aba_cadastro:

        st.subheader("Criar Conta")

        nome = st.text_input(
            "Nome"
        )

        email = st.text_input(
            "Email",
            key="cadastro_email"
        )

        senha = st.text_input(
            "Senha",
            type="password",
            key="cadastro_senha"
        )

        if st.button(
            "Criar Conta",
            use_container_width=True
        ):

            resposta = cadastrar_usuario(
                nome,
                email,
                senha
            )

            if resposta and resposta.user:

                # ==============================
                # LOGIN AUTOMÁTICO
                # ==============================

                st.session_state.usuario = resposta.user

                st.success(
                    "✅ Conta criada com sucesso!"
                )

                st.rerun()

    st.stop()

# ======================================
# TÍTULO
# ======================================

st.title("💰 Preço Certo")

st.caption(
    "Precifique com inteligência."
)

# ======================================
# USUÁRIO LOGADO
# ======================================

col_user, col_logout = st.columns([6, 1])

with col_user:

    st.success(
        f"✅ Usuário conectado: {st.session_state.usuario.email}"
    )

with col_logout:

    if st.button("Sair"):

        logout_usuario()

        st.rerun()

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
    # OBJETIVO DE LUCRO
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

        if "erro" in resultado:

            st.error(resultado["erro"])

        else:

            st.metric(
                "🏷️ Preço Sugerido",
                formatar_moeda(resultado['preco_sugerido'])
            )

            st.metric(
                "💰 Lucro Líquido",
                formatar_moeda(resultado['lucro'])
            )

            st.metric(
                "⚙️ Markup",
                f"{resultado['markup']}x"
            )