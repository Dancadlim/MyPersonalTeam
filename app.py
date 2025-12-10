import streamlit as st
import google.generativeai as genai
import time
from fpdf import FPDF
import os

# --- CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="Holistic Health AI", layout="wide")

# Inicializa variáveis de sessão (Estado)
if 'pagina_atual' not in st.session_state:
    st.session_state.pagina_atual = 'landing'
if 'plano_final' not in st.session_state:
    st.session_state.plano_final = ""
if 'dados_usuario' not in st.session_state:
    st.session_state.dados_usuario = {}
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Configuração da API (Se estiver rodando local, use st.secrets ou variável de ambiente)
# Para o MVP rápido, pode pedir a chave na tela se preferir, ou hardcoded para teste local
# os.environ["GOOGLE_API_KEY"] = "SUA_CHAVE_AQUI" 
# genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# --- FUNÇÕES AUXILIARES ---

def gerar_pdf(texto_plano):
    """Gera um PDF simples com o plano."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Tratamento simples para caracteres (o FPDF básico pode ter problemas com acentos)
    # Para um MVP robusto, recomenda-se usar bibliotecas que suportam UTF-8 melhor
    for linha in texto_plano.split('\n'):
        pdf.multi_cell(0, 10, txt=linha.encode('latin-1', 'replace').decode('latin-1'))
    return pdf.output(dest='S').encode('latin-1')

def simular_agentes(dados):
    """
    Aqui vai a lógica do NOSSO LOOP MANUAL (Personal -> Fisio -> Nutri -> Coach).
    Por enquanto, vou colocar um placeholder para o front-end funcionar.
    """
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Simulação da conversa (Substitua pelo seu código do Loop While depois)
    status_text.text("Personal Trainer está analisando seu perfil...")
    time.sleep(2)
    progress_bar.progress(25)
    
    status_text.text("Fisioterapeuta está revisando segurança articular...")
    time.sleep(2)
    progress_bar.progress(50)
    
    status_text.text("Nutricionista está calculando macros...")
    time.sleep(2)
    progress_bar.progress(75)
    
    status_text.text("Coach de Bem-Estar está consolidando o plano...")
    time.sleep(2)
    progress_bar.progress(100)
    status_text.text("Plano Pronto!")
    
    # Retorna um texto fictício por enquanto
    return f"""
    # SEU PLANO PERSONALIZADO
    **Objetivo:** {dados.get('objetivo')}
    
    ## 1. Treino (Aprovado pelo Fisio)
    - Treino A: Peito e Tríceps
    - Treino B: Costas e Bíceps
    
    ## 2. Nutrição
    - Calorias: 2500kcal
    - Orçamento: {dados.get('orcamento_nutri')}
    
    ## 3. Bem-Estar
    - Dormir 8h por dia.
    - Beber 3L de água.
    """

# --- PÁGINAS DO APLICATIVO ---

def pagina_landing():
    st.title("Bem-vindo ao Holistic Health AI")
    st.subheader("Sua equipe multidisciplinar de saúde, potencializada por IA.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("""
        Imagine ter um Personal Trainer, um Nutricionista, um Fisioterapeuta e um Coach 
        trabalhando JUNTOS para criar sua rotina perfeita.
        
        Nossa IA simula uma junta médica que debate seu caso até chegar na solução ideal.
        """)
        if st.button("Começar Minha Transformação"):
            st.session_state.pagina_atual = 'anamnese'
            st.rerun()
    with col2:
        st.info("Imagem ilustrativa dos 4 agentes conversando aqui.")

def pagina_anamnese():
    st.title("Conte-nos sobre você")
    st.write("Para que nossa equipe possa ajudar, precisamos de detalhes.")
    
    with st.form("form_anamnese"):
        # Dados Pessoais
        col1, col2 = st.columns(2)
        nome = col1.text_input("Nome")
        idade = col2.number_input("Idade", min_value=16, max_value=90)
        
        # Treino
        st.subheader("Treino e Rotina")
        dias_treino = st.slider("Quantos dias pode treinar na semana?", 1, 7, 4)
        experiencia = st.selectbox("Nível de Experiência", ["Iniciante", "Intermediário", "Avançado"])
        lesoes = st.text_area("Possui alguma lesão ou dor? (Importante para o Fisioterapeuta)")
        
        # Nutrição
        st.subheader("Nutrição")
        objetivo = st.selectbox("Qual seu objetivo principal?", ["Emagrecer", "Hipertrofia", "Manutenção", "Performance"])
        orcamento_nutri = st.selectbox("Orçamento mensal para alimentação", ["Baixo (Básico)", "Médio", "Alto (Livre)"])
        restricoes = st.text_input("Alergias ou alimentos que não come")
        
        submitted = st.form_submit_button("Gerar Meu Plano com IA")
        
        if submitted:
            # Salva no estado
            st.session_state.dados_usuario = {
                "nome": nome,
                "dias_treino": dias_treino,
                "lesoes": lesoes,
                "objetivo": objetivo,
                "orcamento_nutri": orcamento_nutri
            }
            
            # Roda a simulação (Aqui entra a sua lógica pesada depois)
            with st.spinner("Convocando a equipe de especialistas..."):
                plano = simular_agentes(st.session_state.dados_usuario)
                st.session_state.plano_final = plano
                st.session_state.pagina_atual = 'dashboard'
                st.rerun()

def pagina_dashboard():
    st.title(f"Painel de Controle de {st.session_state.dados_usuario.get('nome', 'Usuário')}")
    
    tab1, tab2, tab3 = st.tabs(["Meu Plano", "Diário & Metas", "Assistente IA"])
    
    # TAB 1: O Plano (PDF e Texto)
    with tab1:
        st.success("Seu plano foi gerado com sucesso pela equipe!")
        st.download_button(
            label="Baixar Plano em PDF",
            data=gerar_pdf(st.session_state.plano_final),
            file_name="meu_plano_holistico.pdf",
            mime="application/pdf"
        )
        st.markdown("---")
        st.markdown(st.session_state.plano_final)
        
    # TAB 2: Os "Ticks" (Checklist Diário)
    with tab2:
        st.header("Metas de Hoje")
        st.write("Marque o que você completou hoje para alimentar suas estatísticas.")
        
        col1, col2, col3 = st.columns(3)
        check_treino = col1.checkbox("🏋️ Fiz o Treino")
        check_dieta = col2.checkbox("🥦 Segui a Dieta")
        check_agua = col3.checkbox("💧 Bebi Água")
        
        if st.button("Salvar Progresso do Dia"):
            st.toast("Progresso salvo! (Simulação)")
            # Aqui você salvaria num banco de dados ou JSON
            
        st.markdown("### Suas Estatísticas")
        st.bar_chart({"Treino": 5, "Dieta": 4, "Água": 6}) # Dados fictícios
        
    # TAB 3: O Chatbot de Acompanhamento
    with tab3:
        st.header("Converse com seu Assistente")
        st.write("Dúvidas sobre o plano? Pergunte aqui.")
        
        # Histórico do Chat
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Input do usuário
        if prompt := st.chat_input("Ex: Posso comer chocolate hoje?"):
            # Adiciona msg do usuário
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Resposta da IA (Simples por enquanto)
            with st.chat_message("assistant"):
                resposta_ia = f"Com base no seu plano de {st.session_state.dados_usuario.get('objetivo')}, a resposta é..."
                st.markdown(resposta_ia)
                st.session_state.chat_history.append({"role": "assistant", "content": resposta_ia})

# --- ROTEAMENTO ---

if st.session_state.pagina_atual == 'landing':
    pagina_landing()
elif st.session_state.pagina_atual == 'anamnese':
    pagina_anamnese()
elif st.session_state.pagina_atual == 'dashboard':
    pagina_dashboard()
