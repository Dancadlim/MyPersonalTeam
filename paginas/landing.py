import streamlit as st
from db_manager import listar_usuarios, buscar_usuario, ler_plano_recente

def mostrar_landing():
    st.title("Bem-vindo ao My Personal Team 🧬")
    st.write("Sua equipe de saúde multidisciplinar composta por Agentes de IA.")

    # Opção para carregar perfil existente
    usuarios_existentes = listar_usuarios()
    
    col_new, col_load = st.columns(2)
    
    with col_new:
        st.subheader("Novo Usuário")
        if st.button("🚀 Iniciar Nova Anamnese"):
            st.session_state.pagina_atual = 'anamnese'
            st.rerun()
            
    with col_load:
        st.subheader("Carregar Perfil")
        if usuarios_existentes:
            usuario_selecionado = st.selectbox("Selecione seu perfil:", [""] + usuarios_existentes)
            if usuario_selecionado and st.button("📂 Carregar"):
                user_id, dados = buscar_usuario(usuario_selecionado)
                if dados:
                    st.session_state.dados_usuario = dados
                    # Tenta carregar o plano
                    plano = ler_plano_recente(user_id)
                    if plano:
                        st.session_state.plano_final = plano
                        st.session_state.pagina_atual = 'dashboard'
                        st.toast(f"Bem-vindo de volta, {usuario_selecionado}!")
                        st.rerun()
                    else:
                        st.warning("Perfil encontrado, mas sem plano salvo.")
        else:
            st.info("Nenhum perfil salvo ainda.")
            
    st.divider()
    if st.button("🛠️ Admin"):
        st.session_state.pagina_atual = 'admin'
        st.rerun()
