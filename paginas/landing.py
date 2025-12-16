import streamlit as st

def mostrar_landing():
    st.markdown("""
        <h1 style='text-align: center; color: #2E86C1;'>My Personal Team 🚀</h1>
        <h3 style='text-align: center;'>Sua Junta Médica de Inteligência Artificial.</h3>
        <hr>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1: st.info("📝 **1. Você conta sua história**"); st.write("Preencha a anamnese.")
    with col2: st.warning("🤖 **2. A Equipe se reúne**"); st.write("4 Agentes debatem.")
    with col3: st.success("📄 **3. Seu Plano Holístico**"); st.write("Treino + Dieta + Chat.")

    st.markdown("---")
    st.markdown("### 🏆 Sua nova equipe")
    c1, c2, c3, c4 = st.columns(4)
    c1.container(border=True).markdown("### 🏋️ Personal")
    c2.container(border=True).markdown("### 🩺 Fisio")
    c3.container(border=True).markdown("### 🍎 Nutri")
    c4.container(border=True).markdown("### 🧘 Coach")

    st.write(""); st.write("")
    
    _, col_btn, _ = st.columns([1, 2, 1])
    if col_btn.button("🚀 CONTRATAR MINHA EQUIPE (Grátis)", use_container_width=True, type="primary"):
        st.session_state.pagina_atual = 'anamnese'
        st.rerun()
