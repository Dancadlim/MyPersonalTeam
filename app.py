import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions
import time
from fpdf import FPDF
import os

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
    # 1. Tenta ler a estrutura [google] -> api_key
    if "google" in st.secrets and "api_key" in st.secrets["google"]:
        api_key = st.secrets["google"]["api_key"]
    # 2. Fallback: Tenta ler se estiver solta
    elif "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
except Exception:
    pass

# Se não encontrar a chave, para o app e avisa
if not api_key:
    st.error("🚨 Erro de Configuração: API Key não detectada.")
    st.info("Configure a chave nos 'Secrets' do Streamlit Cloud.")
    st.stop()

# --- CONFIGURA O GEMINI ---
genai.configure(api_key=api_key)
# Aumentamos o token limit para garantir que a dieta não seja cortada
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 8192, 
}
# Verifique se o modelo "gemini-2.5-flash-lite" está disponível na sua conta. 
# Caso contrário, use "gemini-1.5-flash" ou "gemini-1.5-pro".
model = genai.GenerativeModel(model_name="gemini-2.5-flash-lite",
                              generation_config=generation_config)


# --- 2. PROMPTS DOS ESPECIALISTAS (VERSÃO BLINDADA) ---

PROMPT_PERSONAL = """
Você é um Personal Trainer de elite.
TAREFA: Criar um plano de treino detalhado baseado na ROTINA e OBJETIVO do usuário.
INPUT: Dados do usuário e histórico.
SAÍDA OBRIGATÓRIA:
1. Se for a primeira vez, crie o treino (Exercício, Séries, Repetições, Descanso).
2. Se estiver revisando após feedback do Fisio, AJUSTE o treino.
3. Se todos concordarem, comece com 'ok'.
"""

PROMPT_FISIO = """
Você é um Fisioterapeuta Esportivo.
TAREFA: Garantir a segurança do usuário.
INPUT: Plano de treino atual + Histórico de lesões.
SAÍDA OBRIGATÓRIA:
1. Analise cada exercício proposto pelo Personal contra as lesões do usuário.
2. Se houver risco: VETE e sugira a substituição (ex: "Trocar Agachamento por Leg Press").
3. Se seguro: APROVE (comece com 'ok') e adicione uma seção de "Mobilidade/Aquecimento Obrigatório".
IMPORTANTÍSSIMO: Mantenha o treino aprovado no texto da sua resposta.
"""

PROMPT_NUTRI = """
Você é um Nutricionista Esportivo.
TAREFA: Criar um cardápio diário COMPLETO e anexá-lo ao plano.
INPUT: Dados do usuário (peso, altura, rotina, gostos) + Plano de Treino/Fisio aprovado.
REGRAS CRÍTICAS:
1. Você NÃO pode apenas dar dicas. Você tem que montar o cardápio: Café, Almoço, Lanche, Jantar.
2. Calcule estimativa de Calorias e Proteínas baseada no peso/altura/objetivo.
3. Considere a ingestão de ÁGUA informada e ajuste a meta hídrica se necessário.
4. O plano de treino e fisio ANTERIOR não pode sumir. VOCÊ DEVE REPETI-LO.
SAÍDA OBRIGATÓRIA:
- Repita o Plano de Treino/Fisio Integralmente.
- Adicione: "## 🍎 PLANO NUTRICIONAL DIÁRIO"
- Liste as refeições com quantidades (ex: 150g de frango).
"""

PROMPT_MEDICO_GERAL = """
Você é um Coach de Saúde Holística (Gerente do Projeto).
TAREFA: Consolidar, formatar e dar o polimento final.
INPUT: O documento contendo Treino + Mobilidade + Dieta.
REGRAS CRÍTICAS:
1. Verifique se a DIETA está presente. Se não estiver, invente uma baseada nos dados (mas para este MVP, garanta que ela apareça).
2. Adicione seção de "Bem-Estar": Sono, Hidratação (calcule ML ideal vs atual), Estresse.
3. Formate tudo em Markdown limpo.
4. Sua resposta é o PRODUTO FINAL. Não resuma demais, o usuário precisa dos detalhes.
"""

# --- 3. FUNÇÕES AUXILIARES ---

def gerar_pdf(texto_plano):
    """Gera um PDF simples com o plano."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Plano de Saude Holistica - IA", ln=1, align='C')
    pdf.ln(10)
    
    # Tratamento básico de texto para o FPDF (latin-1)
    # Substitui caracteres que costumam quebrar o FPDF básico
    try:
        texto_limpo = texto_plano.encode('latin-1', 'replace').decode('latin-1')
    except:
        texto_limpo = texto_plano # Fallback simples
    
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 6, txt=texto_limpo)
    
    return pdf.output(dest='S').encode('latin-1')

def chamar_especialista(persona_prompt, historico_conversa, tarefa_atual, status_container):
    """
    Chama a API do Gemini com lógica de retry.
    """
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

def simular_agentes(d):
    """Executa o LOOP de agentes."""
    
    # Descrição Rica com os novos campos de texto livre
    desc_user = f"""
    PERFIL: {d['nome']}, {d['idade']} anos, {d['sexo']}.
    CORPO: {d['peso']}kg, {d['altura']}cm.
    
    OBJETIVO PRINCIPAL (Texto Livre): {d['objetivo_detalhado']}
    
    ROTINA SEMANAL DETALHADA: 
    "{d['rotina_texto']}"
    
    LOGÍSTICA TREINO: {d['dias_treino']}x na semana. Dispõe de {d['tempo_treino']} min/dia.
    Local: {d['local_treino']}. Exp: {d['experiencia']}.
    
    SAÚDE/LIMITAÇÕES: {d['lesoes']}. Condições: {d['saude_geral']}.
    
    NUTRIÇÃO:
    - Cozinha? {d['cozinha']}.
    - Refeições/dia: {d['refeicoes_dia']}.
    - Água atual: {d['agua_atual']} Litros/dia.
    - Orçamento: {d['orcamento']}.
    - Não come: {d['restricoes']}.
    - Suplementa? {d['suplementos']}.
    
    ESTILO DE VIDA:
    - Trabalho: {d['trabalho']}.
    - Sono: {d['sono']}h/noite.
    - Stress (0-10): {d['estresse']}.
    """

    consenso_atingido = False
    historico_conversa = f"Paciente: {desc_user}\n"
    plano_atual = "Nenhum plano criado ainda."
    max_ciclos = 2 # MVP: 2 ciclos para ser rápido, mas suficiente para correção
    ciclo_atual = 0
    
    with st.status("Reunião do Conselho Multidisciplinar...", expanded=True) as status:
        while not consenso_atingido and ciclo_atual < max_ciclos:
            ciclo_atual += 1
            status.write(f"--- 🔄 Ciclo de Revisão {ciclo_atual} ---")
            
            respostas_comecam_com_ok = []

            # --- PERSONAL ---
            status.write("🏋️ **Personal Trainer** está analisando sua rotina...")
            resp_personal = chamar_especialista(PROMPT_PERSONAL, historico_conversa, f"Criar/ajustar plano baseado na rotina. Atual: {plano_atual}", status)
            plano_atual = resp_personal
            historico_conversa += f"Personal Trainer: {resp_personal}\n"
            respostas_comecam_com_ok.append(resp_personal.lower().startswith('ok'))
            
            # --- FISIO ---
            status.write("🩺 **Fisioterapeuta** está verificando segurança...")
            resp_fisio = chamar_especialista(PROMPT_FISIO, historico_conversa, f"Validar segurança. Atual: {plano_atual}", status)
            plano_atual = resp_fisio
            historico_conversa += f"Fisioterapeuta: {resp_fisio}\n"
            respostas_comecam_com_ok.append(resp_fisio.lower().startswith('ok'))
            
            # --- NUTRI ---
            status.write("🍎 **Nutricionista** está montando o cardápio...")
            resp_nutri = chamar_especialista(PROMPT_NUTRI, historico_conversa, f"Inserir Dieta Detalhada mantendo o treino. Atual: {plano_atual}", status)
            plano_atual = resp_nutri
            historico_conversa += f"Nutricionista: {resp_nutri}\n"
            respostas_comecam_com_ok.append(resp_nutri.lower().startswith('ok'))
            
            # --- COACH ---
            status.write("🧘 **Coach de Bem-Estar** está consolidando o relatório...")
            resp_medico = chamar_especialista(PROMPT_MEDICO_GERAL, historico_conversa, f"Formatar Plano Final Completo. Atual: {plano_atual}", status)
            plano_atual = resp_medico
            historico_conversa += f"Coach: {resp_medico}\n"
            respostas_comecam_com_ok.append(resp_medico.lower().startswith('ok'))
            
            if all(respostas_comecam_com_ok):
                consenso_atingido = True
                status.update(label="🎉 Consenso Atingido! Plano pronto.", state="complete", expanded=False)
            else:
                status.warning(f"⚠️ Ajustes necessários. Reiniciando ciclo...")
        
        if not consenso_atingido:
            status.update(label="⚠️ Entregando melhor versão disponível.", state="error")
            
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
        
        if st.button("Começar Minha Transformação", type="primary"):
            st.session_state.pagina_atual = 'anamnese'
            st.rerun()
            
    with col2:
        st.info("🤖 Personal Trainer\n\n🩺 Fisioterapeuta\n\n🍎 Nutricionista\n\n🧘 Coach de Bem-Estar")

def pagina_anamnese():
    st.title("Anamnese Profissional")
    st.info("Quanto mais detalhes sobre sua rotina, mais a IA consegue adaptar o plano.")
    
    with st.form("form_completo"):
        
        with st.expander("1. Quem é você?", expanded=True):
            c1, c2, c3 = st.columns(3)
            nome = c1.text_input("Nome")
            idade = c2.number_input("Idade", 16, 90, 25)
            sexo = c3.selectbox("Sexo Biológico", ["Masculino", "Feminino"])
            
            c4, c5 = st.columns(2)
            peso = c4.number_input("Peso (kg)", 40.0, 200.0, 70.0)
            altura = c5.number_input("Altura (cm)", 100, 230, 170)
            
            # CAMPO DE TEXTO LIVRE PARA OBJETIVO
            objetivo_detalhado = st.text_area(
                "Qual seu objetivo principal? Pratica algum esporte?", 
                placeholder="Ex: Quero hipertrofia, mas jogo Tênis aos sábados e preciso de agilidade. Ou: Quero só emagrecer e não pratico nada."
            )

        with st.expander("2. Sua Realidade (Rotina e Treino)", expanded=True):
            # CAMPO DE TEXTO LIVRE PARA ROTINA
            st.markdown("**Descreva sua rotina típica de Segunda a Sexta:**")
            rotina_texto = st.text_area(
                "Rotina Diária", 
                height=150,
                placeholder="Ex: Acordo as 7h, pego 1h de ônibus, trabalho sentado até 18h. Almoço em restaurante por quilo. Tenho tempo livre à noite..."
            )
            
            c1, c2 = st.columns(2)
            local_treino = c1.selectbox("Onde vai treinar?", ["Academia Completa", "Academia de Prédio", "Em Casa (Peso do corpo)", "Em Casa (Equipado)", "Parque/Ar Livre"])
            experiencia = c2.selectbox("Nível na Musculação", ["Sedentário", "Iniciante", "Intermediário", "Avançado"])
            
            c3, c4 = st.columns(2)
            dias_treino = c3.slider("Dias disponíveis p/ Musculação", 1, 7, 4)
            tempo_treino = c4.slider("Minutos disponíveis por treino", 20, 120, 60)
            
            lesoes = st.text_area("🚑 Lesões ou Dores?", placeholder="Ex: Dor no ombro direito ao elevar o braço...")

        with st.expander("3. Nutrição e Hábitos"):
            c1, c2 = st.columns(2)
            cozinha = c1.selectbox("Você cozinha?", ["Sim, gosto", "Sim, o básico", "Não, compro pronto/marmita"])
            refeicoes_dia = c2.selectbox("Quantas refeições prefere?", ["3 (Café, Almoço, Jantar)", "4 (+ Lanche)", "5 ou 6 (Várias pequenas)"])
            
            c3, c4 = st.columns(2)
            orcamento = c3.selectbox("Orçamento Alimentar", ["Econômico (Ovos, Frango, Batata)", "Médio", "Alto (Salmão, Suplementos, etc)"])
            # --- NOVO CAMPO DE ÁGUA ---
            agua_atual = c4.number_input("Quantos litros de água bebe por dia?", 0.0, 6.0, 1.5, step=0.1)
            
            suplementos = st.text_input("Toma ou tomaria suplementos?", placeholder="Ex: Whey, Creatina...")
            restricoes = st.text_area("O que NÃO come?", placeholder="Ex: Odeio fígado, sou intolerante a lactose...")

        with st.expander("4. Estilo de Vida (Opcional)"):
            c1, c2, c3 = st.columns(3)
            trabalho = c1.selectbox("Tipo de Trabalho", ["Sedentário", "Misto", "Ativo", "Muito Ativo"])
            sono = c2.number_input("Horas de sono", 4, 12, 7)
            estresse = c3.slider("Nível de Estresse (0-10)", 0, 10, 5)
            saude_geral = st.text_input("Condições de saúde", placeholder="Diabetes, Hipertensão...")

        submitted = st.form_submit_button("Gerar Plano Holístico")
        
        if submitted:
            # Cria o dicionário completo
            d = {
                "nome": nome, "idade": idade, "sexo": sexo, "peso": peso, "altura": altura,
                "objetivo_detalhado": objetivo_detalhado,
                "rotina_texto": rotina_texto,
                "local_treino": local_treino, "experiencia": experiencia, 
                "dias_treino": dias_treino, "tempo_treino": tempo_treino,
                "lesoes": lesoes, "cozinha": cozinha, "refeicoes_dia": refeicoes_dia,
                "orcamento": orcamento, "suplementos": suplementos, "restricoes": restricoes,
                "trabalho": trabalho, "sono": sono, "estresse": estresse, "saude_geral": saude_geral,
                "agua_atual": agua_atual # Adicionado ao dicionário
            }
            st.session_state.dados_usuario = d
            st.session_state.plano_final = simular_agentes(d)
            st.session_state.pagina_atual = 'dashboard'
            st.rerun()

def pagina_dashboard():
    nome = st.session_state.dados_usuario.get('nome', 'Usuário')
    st.title(f"Painel de {nome}")
    
    if st.button("⬅️ Refazer"):
        st.session_state.pagina_atual = 'landing'
        st.rerun()
    
    tab1, tab2, tab3 = st.tabs(["📋 Meu Plano Oficial", "✅ Check-in Diário", "💬 Assistente Pessoal"])
    
    # TAB 1: O Plano
    with tab1:
        st.success("Este plano foi aprovado por consenso da equipe.")
        col_btn, col_info = st.columns([1, 4])
        with col_btn:
            try:
                pdf_bytes = gerar_pdf(st.session_state.plano_final)
                st.download_button("📥 Baixar PDF", pdf_bytes, "plano_holistico.pdf", "application/pdf")
            except Exception:
                st.warning("Erro ao gerar PDF (caracteres especiais).")
        st.markdown("---")
        st.markdown(st.session_state.plano_final)
        
    # TAB 2: Check-in
    with tab2:
        st.header("Metas de Hoje")
        c1, c2, c3 = st.columns(3)
        c1.checkbox("🏋️ Treino Realizado")
        c2.checkbox("🍎 Dieta 100%")
        c3.checkbox("😴 Dormi bem")
        if st.button("Salvar Dia"):
            st.toast("Progresso registrado! (Simulação)")

    # TAB 3: Chatbot com Seleção de Especialista e Edição
    with tab3:
        st.header("Consultoria & Ajustes")
        st.info("Converse com um especialista específico para tirar dúvidas ou PEDIR MUDANÇAS no plano.")

        # 1. Seletor de Especialista
        tipo_especialista = st.selectbox(
            "Com quem você quer falar?",
            ["Equipe Completa (Geral)", "Personal Trainer (Treino)", "Nutricionista (Dieta)", "Fisioterapeuta (Dores/Mobilidade)", "Coach (Sono/Rotina)"]
        )

        # Mostra histórico
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ex: Não gosto de batata doce, troque por arroz no almoço."):
            # Adiciona msg do usuario
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            if model:
                with st.chat_message("assistant"):
                    with st.spinner(f"{tipo_especialista} está analisando..."):
                        
                        # PROMPT AVANÇADO PARA EDIÇÃO
                        prompt_sistema = f"""
                        Você está atuando como: {tipo_especialista}.
                        
                        O PLANO ATUAL DO USUÁRIO É ESTE:
                        --- INICIO PLANO ---
                        {st.session_state.plano_final}
                        --- FIM PLANO ---

                        O USUÁRIO DISSE: "{prompt}"

                        SUA MISSÃO:
                        1. Se for uma dúvida simples, apenas responda.
                        2. Se o usuário pedir para MUDAR algo (ex: trocar alimento, mudar dia de treino, ajustar horário):
                           - Você DEVE reescrever a parte necessária do plano.
                           - Você deve manter o restante do plano que não foi afetado.
                           - Você DEVE analisar se a mudança solicitada quebra alguma regra (ex: Fisio vetar exercício perigoso).
                        
                        FORMATO DE RESPOSTA OBRIGATÓRIO (PARA MUDANÇAS):
                        Se você alterou o plano, no final da sua explicação, você DEVE imprimir o PLANO COMPLETO E ATUALIZADO dentro das tags:
                        <PLANO_ATUALIZADO>
                        ... cole o texto completo do novo plano aqui ...
                        </PLANO_ATUALIZADO>
                        """

                        try:
                            response = model.generate_content(prompt_sistema)
                            texto_resposta = response.text
                            
                            # Lógica para detectar se houve mudança de plano
                            if "<PLANO_ATUALIZADO>" in texto_resposta:
                                # Extrai o novo plano
                                partes = texto_resposta.split("<PLANO_ATUALIZADO>")
                                explicacao = partes[0] # O que vem antes da tag
                                novo_plano_sujo = partes[1]
                                novo_plano_limpo = novo_plano_sujo.split("</PLANO_ATUALIZADO>")[0].strip()
                                
                                # Atualiza a explicação na tela
                                st.markdown(explicacao)
                                st.session_state.chat_history.append({"role": "assistant", "content": explicacao})
                                
                                # ATUALIZA O ESTADO E RECARREGA
                                st.session_state.plano_final = novo_plano_limpo
                                st.toast("✅ Plano Oficial Atualizado com sucesso!", icon="💾")
                                time.sleep(2) # Dá tempo de ler o toast
                                st.rerun() # Recarrega a página para mostrar o novo plano na Tab 1
                                
                            else:
                                # Resposta normal (apenas conversa)
                                st.markdown(texto_resposta)
                                st.session_state.chat_history.append({"role": "assistant", "content": texto_resposta})
                                
                        except Exception as e:
                            st.error(f"Erro ao responder: {e}")

# Roteador
if st.session_state.pagina_atual == 'landing':
    pagina_landing()
elif st.session_state.pagina_atual == 'anamnese':
    pagina_anamnese()
elif st.session_state.pagina_atual == 'dashboard':
    pagina_dashboard()
