import streamlit as st
from paginas.landing import mostrar_landing
from paginas.anamnese import mostrar_anamnese
from paginas.dashboard import mostrar_dashboard

st.set_page_config(page_title="My Personal Team", page_icon="🧬", layout="wide")

# Inicializa Estado
if 'pagina_atual' not in st.session_state: st.session_state.pagina_atual = 'landing'
if 'plano_final' not in st.session_state: st.session_state.plano_final = ""
if 'dados_usuario' not in st.session_state: st.session_state.dados_usuario = {}
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# Roteador
if st.session_state.pagina_atual == 'landing':
    mostrar_landing()
elif st.session_state.pagina_atual == 'anamnese':
    mostrar_anamnese()
elif st.session_state.pagina_atual == 'dashboard':
    mostrar_dashboard()
