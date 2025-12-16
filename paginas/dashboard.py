import streamlit as st
import time
from agentes import gerar_pdf, configurar_google_api

def mostrar_dashboard():
    nome = st.session_state.dados_usuario.get('nome', 'Usuário')
    st.title(f"Painel de {nome}")
    
    if st.button("⬅️ Início"):
        st.session_state.pagina_atual = 'landing'
        st.rerun()
    
    tab1, tab2, tab3 = st.tabs(["📋 Plano", "✅ Check-in", "💬 Chat"])
    
    with tab1:
        st.success("Plano Aprovado.")
        try:
            pdf_bytes = gerar_pdf(st.session_state.plano_final)
            st.download_button("📥 Baixar PDF", pdf_bytes, "plano.pdf", "application/pdf")
        except: st.warning("Erro PDF.")
        st.markdown(st.session_state.plano_final)
        
    with tab2:
        st.header("Hoje")
        c1, c2, c3 = st.columns(3)
        c1.checkbox("Treino"); c2.checkbox("Dieta"); c3.checkbox("Sono")
        if st.button("Salvar"): st.toast("Salvo!")

    with tab3:
        st.header("Assistente")
        model = configurar_google_api()
        
        for msg in st.session_state.chat_history:
            st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input("Dúvida?"):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            
            if model:
                with st.chat_message("assistant"):
                    with st.spinner("Pensando..."):
                        ctx = f"Plano atual:\n{st.session_state.plano_final}\nUsuário disse: {prompt}"
                        resp = model.generate_content(ctx).text
                        st.write(resp)
                        st.session_state.chat_history.append({"role": "assistant", "content": resp})
