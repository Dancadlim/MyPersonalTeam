import streamlit as st
import sqlite3
import pandas as pd
from db_manager import DB_NAME

def mostrar_admin():
    st.title("🛠️ Área Administrativa do Banco de Dados")
    
    conn = sqlite3.connect(DB_NAME)
    
    st.subheader("Usuários Cadastrados")
    try:
        df_users = pd.read_sql_query("SELECT * FROM usuarios", conn)
        st.dataframe(df_users)
    except:
        st.warning("Nenhum usuário encontrado.")
        
    st.subheader("Planos Gerados")
    try:
        df_planos = pd.read_sql_query("SELECT * FROM planos", conn)
        st.dataframe(df_planos)
    except:
        st.warning("Nenhum plano encontrado.")
        
    conn.close()
    
    if st.button("⬅️ Voltar ao Início"):
        st.session_state.pagina_atual = 'landing'
        st.rerun()
