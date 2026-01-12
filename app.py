import streamlit as st
from paginas.landing import mostrar_landing
from paginas.anamnese import mostrar_anamnese
from paginas.dashboard import mostrar_dashboard
from paginas.admin import mostrar_admin
from db_manager import init_db

# Inicializa Banco de Dados
init_db()

st.set_page_config(page_title="My Personal Team", page_icon="🧬", layout="wide")

# Custom CSS
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
        font-family: 'Inter', sans-serif;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #FF4B4B, #FF914D);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 75, 75, 0.3);
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #262730;
        border-radius: 8px;
    }
    
    /* Status Container */
    .stStatus {
        border: 1px solid #4B4B4B;
        background-color: #1E1E1E;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

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
elif st.session_state.pagina_atual == 'admin':
    mostrar_admin()
