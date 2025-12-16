import streamlit as st
from agentes import simular_agentes, configurar_google_api

def mostrar_anamnese():
    st.title("Anamnese Profissional")
    model = configurar_google_api()
    if not model:
        st.error("Erro de API Key."); st.stop()

    with st.form("form_completo"):
        with st.expander("1. Quem é você?", expanded=True):
            c1, c2 = st.columns(2)
            nome = c1.text_input("Nome")
            idade = c2.number_input("Idade", 16, 90, 25)
            sexo = st.selectbox("Sexo", ["Masculino", "Feminino"])
            c3, c4 = st.columns(2)
            peso = c3.number_input("Peso", 40.0, 200.0, 70.0)
            altura = c4.number_input("Altura (cm)", 100, 230, 170)
            objetivo_detalhado = st.text_area("Objetivo / Esporte", placeholder="Ex: Hipertrofia, mas jogo tênis...")

        with st.expander("2. Rotina e Treino"):
            rotina_texto = st.text_area("Rotina Diária", height=100, placeholder="Trabalho, horários...")
            local_treino = st.selectbox("Onde treina?", ["Academia", "Casa", "Parque"])
            c1, c2 = st.columns(2)
            dias_treino = c1.slider("Dias/sem", 1, 7, 4)
            tempo_treino = c2.slider("Minutos/treino", 20, 120, 60)
            lesoes = st.text_area("Lesões?", placeholder="Ex: Joelho...")

        with st.expander("3. Nutrição"):
            cozinha = st.selectbox("Cozinha?", ["Sim", "Não"])
            refeicoes_dia = st.selectbox("Refeições/dia", ["3", "4", "5+"])
            agua_atual = st.number_input("Litros de água/dia", 0.0, 6.0, 2.0)
            orcamento = st.selectbox("Orçamento", ["Baixo", "Médio", "Alto"])
            restricoes = st.text_input("Não come?", placeholder="Alergias...")
            suplementos = st.text_input("Suplementos?", placeholder="Whey...")

        with st.expander("4. Estilo de Vida"):
            trabalho = st.selectbox("Trabalho", ["Sedentário", "Ativo"])
            sono = st.number_input("Sono (h)", 4, 12, 7)
            estresse = st.slider("Estresse", 0, 10, 5)
            saude_geral = st.text_input("Saúde Geral", placeholder="Diabetes...")

        if st.form_submit_button("Gerar Plano"):
            d = {
                "nome": nome, "idade": idade, "sexo": sexo, "peso": peso, "altura": altura,
                "objetivo_detalhado": objetivo_detalhado, "rotina_texto": rotina_texto,
                "local_treino": local_treino, "dias_treino": dias_treino, "tempo_treino": tempo_treino,
                "lesoes": lesoes, "cozinha": cozinha, "refeicoes_dia": refeicoes_dia,
                "orcamento": orcamento, "agua_atual": agua_atual, "restricoes": restricoes,
                "suplementos": suplementos, "trabalho": trabalho, "sono": sono, "estresse": estresse, "saude_geral": saude_geral
            }
            st.session_state.dados_usuario = d
            st.session_state.plano_final = simular_agentes(d, model)
            st.session_state.pagina_atual = 'dashboard'
            st.rerun()
