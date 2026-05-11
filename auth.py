import streamlit as st

from supabase_client import supabase

# ======================================
# CADASTRO
# ======================================

def cadastrar_usuario(

    nome,
    email,
    senha

):

    try:

        resposta = supabase.auth.sign_up({

            "email": email,
            "password": senha,

            "options": {

                "data": {

                    "nome": nome

                }

            }

        })

        return resposta

    except Exception as erro:

        st.error(f"Erro ao cadastrar: {erro}")

# ======================================
# LOGIN
# ======================================

def login_usuario(

    email,
    senha

):

    try:

        resposta = supabase.auth.sign_in_with_password({

            "email": email,
            "password": senha

        })

        return resposta

    except Exception as erro:

        st.error(f"Erro no login: {erro}")

# ======================================
# LOGOUT
# ======================================

def logout_usuario():

    supabase.auth.sign_out()

    st.session_state.pop("usuario", None)