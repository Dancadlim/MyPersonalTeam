import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions
import time
from fpdf import FPDF
import os
#
#
#testando as paradas ai
#
# --- 1. CONFIGURAÇÃO DA PÁGINA E API ---
st.set_page_config(page_title="Holistic Health AI", page_icon="🧬", layout="wide")

# Inicializa variáveis de sessão essenciais
if 'pagina_atual' not in st.session_state:
    st.session_state.pagina_atual = 'landing'
if 'plano_final' not in st.session_state:
    st.session_state.plano_final = ""
if 'dados_usuario' not in st.session_state:
    st.session_state.dados_usuario = {}
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# --- LÓGICA DE API KEY (Automática via Secrets) ---
api_key = None

try:
    # Tenta ler a estrutura que você criou na imagem: [google] -> api_key
    if "google" in st.secrets and "api_key" in st.secrets["google"]:
        api_key = st.secrets["google"]["api_key"]
    
    # Fallback: Tenta ler se estiver solta (caso mude depois)
    elif "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        
except Exception as e:
    # Se der erro de leitura (ex: localmente sem arquivo secrets.toml)
    pass

# Se não encontrar a chave, para o app e avisa (sem mostrar campo de input)
if not api_key:
    st.error("🚨 Erro de Configuração: API Key não detectada.")
    st.info("Certifique-se de que a chave está configurada nos 'Secrets' do Streamlit Cloud.")
    st.stop() # Interrompe o código aqui para não dar erro mais para frente

# --- CONFIGURA O GEMINI ---
genai.configure(api_key=api_key)
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 4096,
}
model = genai.GenerativeModel(model_name="gemini-2.5-flash",
                              generation_config=generation_config)


# --- 2. PROMPTS DOS ESPECIALISTAS (CONSTANTES) ---

PROMPT_PERSONAL = """
Você é um Personal Trainer especialista em hipertrofia e performance.
Sua tarefa é criar ou ajustar um plano de treino de 4 dias.
REGRAS:
1. Analise o histórico da conversa e o plano atual.
2. Se o plano estiver perfeito E TODOS os outros especialistas já tiverem concordado no ciclo anterior, comece sua resposta com 'ok'.
3. Se for a primeira rodada ou se ajustes forem necessários, NÃO comece com 'ok'. Comece diretamente com sua proposta de plano de treino.
4. Você DEVE respeitar as limitações do fisioterapeuta.
"""

PROMPT_FISIO = """
Você é um Fisioterapeuta Esportivo focado em prevenção de lesões.
Sua tarefa é revisar o plano de treino do Personal Trainer.
REGRAS:
1. Analise o histórico e o plano atual, focando nas lesões ou dores citadas pelo usuário.
2. Se o plano de treino proposto for 100% seguro e você concordar, comece sua resposta com 'ok' e repita o plano de treino aprovado.
3. Se você tiver QUALQUER ressalva (ex: exercício perigoso para a lesão citada), NÃO comece com 'ok'. Comece sua resposta com suas objeções e proponha um plano modificado.
"""

PROMPT_NUTRI = """
Você é um Nutricionista Esportivo.
Sua tarefa é adicionar um plano nutricional ao plano de treino/fisio.
REGRAS:
1. Analise o histórico e o plano de treino/fisio atual.
2. Crie um plano nutricional que SE INTEGRE ao plano atual, respeitando o orçamento e preferências.
3. Se você concordar com o plano de treino e seu plano de dieta for apenas um acréscimo, comece sua resposta com 'ok'.
4. Se o plano de treino for tão intenso que exija mudanças drásticas na dieta que pareçam irreais, você pode vetar (não comece com 'ok').
5. Sua resposta final deve conter O PLANO COMPLETO (Treino + Nutrição).
"""

PROMPT_MEDICO_GERAL = """
Você é um Coach de Saúde Holística (Bem-Estar Geral).
Sua tarefa é revisar o plano consolidado (treino + nutrição) e cuidar do bem-estar.
REGRAS:
1. Analise o plano completo. Adicione notas sobre sono, gerenciamento de estresse e hidratação.
2. Você é o CONSOLIDADOR FINAL. Sua resposta é o "Plano Oficial" desta rodada.
3. Se o plano integrado (treino + fisio + nutri) parecer coeso e saudável, comece sua resposta com 'ok' e apresente o plano final consolidado formatado em Markdown.
4. Se algo parecer conflitante, NÃO comece com 'ok'. Aponte a falha e mande de volta para revisão.
"""

# --- 3. FUNÇÕES AUXILIARES ---

def gerar_pdf(texto_plano):
    """Gera um PDF simples com o plano."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Plano de Saude Holistica - IA", ln=1, align='C')
    pdf.ln(10)
    # Tratamento básico de texto
    texto_limpo = texto_plano.encode('latin-1', 'replace').decode('latin-1')
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10, txt=texto_limpo)
    return pdf.output(dest='S').encode('latin-1')

def chamar_especialista(persona_prompt, historico_conversa, tarefa_atual, status_container):
    """
    Chama a API do Gemini com lógica de retry, atualizando a UI do Streamlit.
    """
    if not model:
        status_container.error("Erro: Modelo não inicializado (API Key ausente).")
        return "ERRO"

    prompt_completo = f"""
    {persona_prompt}
    --- HISTÓRICO DA DISCUSSÃO ATÉ AGORA ---
    {historico_conversa}
    ------------------------------------
    TAREFA ATUAL: {tarefa_atual}
    Sua resposta (lembre-se da regra do 'ok'):
    """
    
    max_tentativas = 3
    tentativa_atual = 0
    
    while tentativa_atual < max_tentativas:
        try:
            response = model.generate_content(prompt_completo)
            return response.text.strip()
        except google_exceptions.TooManyRequests:
            tentativa_atual += 1
            status_container.warning(f"Limite de API atingido. Aguardando 20s... (Tentativa {tentativa_atual}/{max_tentativas})")
            time.sleep(20)
        except Exception as e:
            status_container.error(f"Erro na API: {e}")
            raise e
            
    return "ERRO: Não foi possível obter resposta do especialista."

def simular_agentes(dados):
    """Executa o LOOP de agentes."""
    
    descricao_usuario = f"""
    Nome: {dados['nome']}, Idade: {dados.get('idade', 'N/A')}.
    Objetivo: {dados['objetivo']}.
    Dias de Treino Disponíveis: {dados['dias_treino']} dias por semana.
    Experiência: {dados.get('experiencia', 'Iniciante')}.
    Histórico de Lesões/Dores: {dados['lesoes']}.
    Orçamento Nutricional: {dados['orcamento_nutri']}.
    Restrições Alimentares: {dados.get('restricoes', 'Nenhuma')}.
    """

    consenso_atingido = False
    historico_conversa = f"Paciente: {descricao_usuario}\n"
    plano_atual = "Nenhum plano criado ainda."
    max_ciclos = 3 
    ciclo_atual = 0
    
    with st.status("Equipe de Especialistas em Reunião...", expanded=True) as status:
        while not consenso_atingido and ciclo_atual < max_ciclos:
            ciclo_atual += 1
            status.write(f"--- 🔄 Ciclo de Revisão {ciclo_atual} ---")
            
            respostas_comecam_com_ok = []

            # --- PERSONAL ---
            status.write("🏋️ **Personal Trainer** está elaborando o treino...")
            resp_personal = chamar_especialista(PROMPT_PERSONAL, historico_conversa, f"Criar/ajustar plano. Atual: {plano_atual}", status)
            plano_atual = resp_personal
            historico_conversa += f"Personal Trainer: {resp_personal}\n"
            respostas_comecam_com_ok.append(resp_personal.lower().startswith('ok'))
            
            # --- FISIO ---
            status.write("🩺 **Fisioterapeuta** está analisando segurança...")
            resp_fisio = chamar_especialista(PROMPT_FISIO, historico_conversa, f"Revisar segurança. Atual: {plano_atual}", status)
            plano_atual = resp_fisio
            historico_conversa += f"Fisioterapeuta: {resp_fisio}\n"
            respostas_comecam_com_ok.append(resp_fisio.lower().startswith('ok'))
            
            # --- NUTRI ---
            status.write("🍎 **Nutricionista** está calculando a dieta...")
            resp_nutri = chamar_especialista(PROMPT_NUTRI, historico_conversa, f"Revisar/adicionar nutrição. Atual: {plano_atual}", status)
            plano_atual = resp_nutri
            historico_conversa += f"Nutricionista: {resp_nutri}\n"
            respostas_comecam_com_ok.append(resp_nutri.lower().startswith('ok'))
            
            # --- COACH ---
            status.write("🧘 **Coach de Bem-Estar** está consolidando...")
            resp_medico = chamar_especialista(PROMPT_MEDICO_GERAL, historico_conversa, f"Consolidar plano final. Atual: {plano_atual}", status)
            plano_atual = resp_medico
            historico_conversa += f"Coach: {resp_medico}\n"
            respostas_comecam_com_ok.append(resp_medico.lower().startswith('ok'))
            
            if all(respostas_comecam_com_ok):
                consenso_atingido = True
                status.update(label="🎉 Consenso Atingido! Plano pronto.", state="complete", expanded=False)
            else:
                status.warning(f"⚠️ Ajustes necessários. Reiniciando ciclo...")
        
        if not consenso_atingido:
            status.update(label="⚠️ Limite de ciclos atingido. Entregando melhor versão.", state="error")
            
    return plano_atual

# --- 4. INTERFACE DO APLICATIVO (ROTEAMENTO) ---

def pagina_landing():
    st.title("Holistic Health AI 🧬")
    st.subheader("Sua equipe multidisciplinar de saúde, potencializada por IA.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### O fim dos planos genéricos.
        Nossa plataforma simula uma junta médica real. Um Personal Trainer, um Nutricionista, 
        um Fisioterapeuta e um Coach de Bem-Estar debatem o seu caso até chegarem 
        na solução perfeita.
        """)
        
        # Só habilita o botão se a API key estiver presente
        if api_key:
            if st.button("Começar Minha Transformação", type="primary"):
                st.session_state.pagina_atual = 'anamnese'
                st.rerun()
        else:
            st.error("🔒 Para começar, insira sua API Key na barra lateral à esquerda.")
            
    with col2:
        st.info("🤖 Personal Trainer\n\n🩺 Fisioterapeuta\n\n🍎 Nutricionista\n\n🧘 Coach de Bem-Estar")

def pagina_anamnese():
    st.title("Anamnese Inteligente")
    st.write("Preencha os dados para que nossa equipe possa iniciar a reunião.")
    
    with st.form("form_anamnese"):
        col1, col2 = st.columns(2)
        nome = col1.text_input("Seu Nome")
        idade = col2.number_input("Idade", min_value=16, max_value=90, value=25)
        
        st.subheader("Treino & Corpo")
        c1, c2, c3 = st.columns(3)
        dias_treino = c1.slider("Dias p/ Treinar (Semana)", 1, 7, 4)
        experiencia = c2.selectbox("Experiência", ["Iniciante", "Intermediário", "Avançado", "Atleta"])
        objetivo = c3.selectbox("Objetivo", ["Hipertrofia", "Emagrecimento", "Performance", "Saúde"])
        
        lesoes = st.text_area("🚑 Histórico de Lesões ou Dores (Importante para o Fisio)", 
                              placeholder="Ex: Tenho condromalácia no joelho esquerdo...")
        
        st.subheader("Nutrição")
        orcamento_nutri = st.selectbox("Orçamento para Dieta", ["Econômico (Ovos/Frango/Raízes)", "Médio", "Alto (Livre)"])
        restricoes = st.text_input("Alergias ou Restrições Alimentares", placeholder="Ex: Intolerante a lactose, não gosto de peixe...")
        
        submitted = st.form_submit_button("Convocar Especialistas e Gerar Plano")
        
        if submitted:
            if not api_key:
                st.error("Configure a API Key antes de continuar.")
            else:
                st.session_state.dados_usuario = {
                    "nome": nome, "idade": idade, "dias_treino": dias_treino,
                    "experiencia": experiencia, "objetivo": objetivo,
                    "lesoes": lesoes, "orcamento_nutri": orcamento_nutri,
                    "restricoes": restricoes
                }
                plano = simular_agentes(st.session_state.dados_usuario)
                st.session_state.plano_final = plano
                st.session_state.pagina_atual = 'dashboard'
                st.rerun()

def pagina_dashboard():
    nome = st.session_state.dados_usuario.get('nome', 'Usuário')
    st.title(f"Painel de {nome}")
    
    if st.button("⬅️ Voltar ao Início"):
        st.session_state.pagina_atual = 'landing'
        st.rerun()
    
    tab1, tab2, tab3 = st.tabs(["📋 Meu Plano Oficial", "✅ Check-in Diário", "💬 Assistente Pessoal"])
    
    # TAB 1
    with tab1:
        st.success("Este plano foi aprovado por consenso da equipe.")
        col_btn, col_info = st.columns([1, 4])
        with col_btn:
            try:
                pdf_bytes = gerar_pdf(st.session_state.plano_final)
                st.download_button("📥 Baixar PDF", pdf_bytes, "plano_holistico.pdf", "application/pdf")
            except Exception:
                st.warning("Erro ao gerar PDF.")
        st.markdown("---")
        st.markdown(st.session_state.plano_final)
        
    # TAB 2
    with tab2:
        st.header("Metas de Hoje")
        c1, c2, c3 = st.columns(3)
        c1.checkbox("🏋️ Treino Realizado")
        c2.checkbox("🍎 Dieta 100%")
        c3.checkbox("😴 Dormi bem")
        if st.button("Salvar Dia"):
            st.toast("Progresso registrado! (Simulação)")

    # TAB 3 (Chatbot)
    with tab3:
        st.header("Tire dúvidas sobre seu plano")
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ex: Posso trocar o arroz por batata hoje?"):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            if model:
                with st.chat_message("assistant"):
                    with st.spinner("Consultando o plano..."):
                        contexto = f"Você é um assistente útil. Responda com base neste plano aprovado: {st.session_state.plano_final}"
                        try:
                            resposta = model.generate_content(f"{contexto}\n\nUsuário: {prompt}").text
                            st.markdown(resposta)
                            st.session_state.chat_history.append({"role": "assistant", "content": resposta})
                        except Exception as e:
                            st.error(f"Erro ao responder: {e}")

# Roteador
if st.session_state.pagina_atual == 'landing':
    pagina_landing()
elif st.session_state.pagina_atual == 'anamnese':
    pagina_anamnese()
elif st.session_state.pagina_atual == 'dashboard':
    pagina_dashboard()
