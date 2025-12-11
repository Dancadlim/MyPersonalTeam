import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions
import time
from fpdf import FPDF
import os

# --- 1. CONFIGURAÇÃO ---
st.set_page_config(page_title="Holistic Health AI", page_icon="🧬", layout="wide")

if 'pagina_atual' not in st.session_state: st.session_state.pagina_atual = 'landing'
if 'plano_final' not in st.session_state: st.session_state.plano_final = ""
if 'dados_usuario' not in st.session_state: st.session_state.dados_usuario = {}
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# --- LÓGICA DE API KEY ---
api_key = None
try:
    if "google" in st.secrets and "api_key" in st.secrets["google"]:
        api_key = st.secrets["google"]["api_key"]
    elif "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
except Exception: pass

if not api_key:
    st.error("🚨 Erro de Configuração: API Key não detectada nos Secrets.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-2.5-flash",
                              generation_config={"temperature": 0.7, "max_output_tokens": 8192})

# --- 2. PROMPTS BLINDADOS (CORREÇÃO DA NUTRIÇÃO) ---

PROMPT_PERSONAL = """
Você é um Personal Trainer de elite.
TAREFA: Criar um plano de treino detalhado.
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
3. O plano de treino e fisio ANTERIOR não pode sumir.
SAÍDA OBRIGATÓRIA:
- Repita o Plano de Treino/Fisio.
- Adicione: "## 🍎 PLANO NUTRICIONAL DIÁRIO"
- Liste as refeições com quantidades (ex: 150g de frango).
"""

PROMPT_MEDICO_GERAL = """
Você é um Coach de Saúde Holística (Gerente do Projeto).
TAREFA: Consolidar, formatar e dar o polimento final.
INPUT: O documento contendo Treino + Mobilidade + Dieta.
REGRAS CRÍTICAS:
1. Verifique se a DIETA está presente. Se não estiver, invente uma baseada nos dados ou mande refazer (mas para este MVP, garanta que ela apareça).
2. Adicione seção de "Bem-Estar": Sono, Hidratação (calcule ML), Estresse.
3. Formate tudo em Markdown limpo para virar PDF depois.
4. Sua resposta é o PRODUTO FINAL. Não resuma demais, o usuário precisa dos detalhes (quantos gramas comer, quantas séries fazer).
"""

# --- 3. FUNÇÕES ---

def gerar_pdf(texto_plano):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Plano Holistico Integrado", ln=1, align='C')
    pdf.ln(10)
    
    # Limpeza básica de caracteres para FPDF (que não suporta emojis/utf-8 complexos nativamente)
    texto_limpo = texto_plano.encode('latin-1', 'replace').decode('latin-1')
    
    # Tenta imprimir linha a linha para evitar quebras gigantes
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 6, txt=texto_limpo)
    
    return pdf.output(dest='S').encode('latin-1')

def chamar_especialista(persona, historico, tarefa, status):
    prompt = f"{persona}\n--- HISTÓRICO ---\n{historico}\n--- TAREFA ---\n{tarefa}"
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        status.error(f"Erro na API: {e}")
        return "Erro ao gerar resposta."

def simular_agentes(d):
    # Montagem da Descrição Expandida
    desc_user = f"""
    PERFIL: {d['nome']}, {d['idade']} anos, {d['sexo']}.
    CORPO: {d['peso']}kg, {d['altura']}cm.
    OBJETIVO: {d['objetivo']} (Prazo: {d['prazo']}).
    
    LOGÍSTICA TREINO: {d['dias_treino']}x na semana. Dispõe de {d['tempo_treino']} min/dia.
    Local: {d['local_treino']}. Exp: {d['experiencia']}.
    
    SAÚDE/LIMITAÇÕES: {d['lesoes']}. Condições: {d['saude_geral']}.
    
    NUTRIÇÃO:
    - Cozinha? {d['cozinha']}.
    - Refeições/dia: {d['refeicoes_dia']}.
    - Orçamento: {d['orcamento']}.
    - Não come: {d['restricoes']}.
    - Suplementa? {d['suplementos']}.
    
    ESTILO DE VIDA:
    - Trabalho: {d['trabalho']}.
    - Sono: {d['sono']}h/noite.
    - Stress (0-10): {d['estresse']}.
    """

    consenso = False
    hist = f"Paciente: {desc_user}\n"
    plano = "Nenhum plano ainda."
    ciclo = 0
    
    with st.status("Reunião do Conselho Multidisciplinar...", expanded=True) as s:
        while not consenso and ciclo < 2: # Limitado a 2 ciclos para o MVP ser rápido
            ciclo += 1
            s.write(f"--- 🔄 Rodada {ciclo} ---")
            oks = []

            s.write("🏋️ **Personal:** Desenhando periodização...")
            resp = chamar_especialista(PROMPT_PERSONAL, hist, f"Criar/Ajustar Treino. Atual: {plano}", s)
            plano = resp
            hist += f"Personal: {resp}\n"
            oks.append(resp.lower().startswith('ok'))

            s.write("🩺 **Fisio:** Verificando biomecânica e riscos...")
            resp = chamar_especialista(PROMPT_FISIO, hist, f"Validar segurança. Atual: {plano}", s)
            plano = resp
            hist += f"Fisio: {resp}\n"
            oks.append(resp.lower().startswith('ok'))

            s.write("🍎 **Nutri:** Calculando macros e cardápio...")
            resp = chamar_especialista(PROMPT_NUTRI, hist, f"Inserir Dieta Detalhada. Atual: {plano}", s)
            plano = resp
            hist += f"Nutri: {resp}\n"
            oks.append(resp.lower().startswith('ok'))

            s.write("🧘 **Coach:** Consolidando relatório final...")
            resp = chamar_especialista(PROMPT_MEDICO_GERAL, hist, f"Formatar Plano Final. Atual: {plano}", s)
            plano = resp
            hist += f"Coach: {resp}\n"
            oks.append(resp.lower().startswith('ok'))

            if all(oks): consenso = True
        
        s.update(label="Plano Finalizado!", state="complete", expanded=False)
    
    return plano

# --- 4. INTERFACE ---

def pagina_landing():
    st.title("Holistic Health AI 2.0 🧬")
    st.write("Sua equipe de saúde completa: Treino, Dieta e Fisioterapia integrados por IA.")
    if st.button("Iniciar Anamnese Completa", type="primary"):
        st.session_state.pagina_atual = 'anamnese'
        st.rerun()

def pagina_anamnese():
    st.title("Anamnese Profissional")
    st.info("Quanto mais detalhes, mais preciso será seu plano.")
    
    with st.form("form_completo"):
        
        with st.expander("1. Biometria e Objetivo", expanded=True):
            c1, c2, c3 = st.columns(3)
            nome = c1.text_input("Nome")
            idade = c2.number_input("Idade", 16, 90, 25)
            sexo = c3.selectbox("Sexo Biológico (p/ cálculo basal)", ["Masculino", "Feminino"])
            
            c4, c5, c6 = st.columns(3)
            peso = c4.number_input("Peso (kg)", 40.0, 200.0, 70.0)
            altura = c5.number_input("Altura (cm)", 100, 230, 170)
            objetivo = c6.selectbox("Objetivo Principal", ["Hipertrofia", "Emagrecimento Agressivo", "Emagrecimento Gradual", "Performance Atlética", "Saúde/Manutenção"])
            prazo = st.text_input("Tem algum prazo/evento?", placeholder="Ex: Casamento em 3 meses, ou 'Sem pressa'")

        with st.expander("2. Rotina de Treino"):
            c1, c2 = st.columns(2)
            local_treino = c1.selectbox("Onde vai treinar?", ["Academia Completa", "Academia de Prédio (Básica)", "Em Casa (Peso do corpo)", "Em Casa (Com alguns equipamentos)"])
            experiencia = c2.selectbox("Nível", ["Sedentário", "Iniciante", "Intermediário", "Avançado"])
            
            c3, c4 = st.columns(2)
            dias_treino = c3.slider("Dias por semana", 1, 7, 4)
            tempo_treino = c4.slider("Minutos disponíveis por treino", 20, 120, 60)
            
            lesoes = st.text_area("🚑 Lesões, dores ou cirurgias passadas?", placeholder="Ex: Dor na lombar ao ficar muito tempo em pé...")

        with st.expander("3. Nutrição e Hábitos"):
            c1, c2 = st.columns(2)
            cozinha = c1.selectbox("Você cozinha?", ["Sim, gosto", "Sim, o básico", "Não, compro pronto/marmita"])
            refeicoes_dia = c2.selectbox("Quantas refeições prefere?", ["3 (Café, Almoço, Jantar)", "4 (+ Lanche)", "5 ou 6 (Várias pequenas)"])
            
            orcamento = st.selectbox("Orçamento Alimentar", ["Econômico (Ovos, Frango, Batata)", "Médio", "Alto (Salmão, Suplementos, etc)"])
            suplementos = st.text_input("Toma ou tomaria suplementos?", placeholder="Ex: Whey, Creatina, ou 'Prefiro só comida'")
            restricoes = st.text_area("O que NÃO come de jeito nenhum? (Alergias ou Gosto)", placeholder="Ex: Odeio fígado, sou intolerante a lactose...")

        with st.expander("4. Estilo de Vida"):
            c1, c2, c3 = st.columns(3)
            trabalho = c1.selectbox("Rotina de Trabalho", ["Sedentário (Escritório)", "Misto", "Ativo (Em pé/Movimento)", "Muito Ativo (Braçal)"])
            sono = c2.number_input("Média de horas de sono", 4, 12, 7)
            estresse = c3.slider("Nível de Estresse (0-10)", 0, 10, 5)
            saude_geral = st.text_input("Alguma condição de saúde?", placeholder="Diabetes, Hipertensão, Ansiedade...")

        if st.form_submit_button("Gerar Plano Holístico"):
            d = {
                "nome": nome, "idade": idade, "sexo": sexo, "peso": peso, "altura": altura,
                "objetivo": objetivo, "prazo": prazo, "local_treino": local_treino,
                "experiencia": experiencia, "dias_treino": dias_treino, "tempo_treino": tempo_treino,
                "lesoes": lesoes, "cozinha": cozinha, "refeicoes_dia": refeicoes_dia,
                "orcamento": orcamento, "suplementos": suplementos, "restricoes": restricoes,
                "trabalho": trabalho, "sono": sono, "estresse": estresse, "saude_geral": saude_geral
            }
            st.session_state.dados_usuario = d
            st.session_state.plano_final = simular_agentes(d)
            st.session_state.pagina_atual = 'dashboard'
            st.rerun()

def pagina_dashboard():
    st.title(f"Plano de {st.session_state.dados_usuario.get('nome')}")
    if st.button("⬅️ Refazer"):
        st.session_state.pagina_atual = 'landing'
        st.rerun()
    
    tab1, tab2 = st.tabs(["📄 Plano Completo", "💬 Tirar Dúvidas"])
    
    with tab1:
        st.markdown(st.session_state.plano_final)
        try:
            pdf = gerar_pdf(st.session_state.plano_final)
            st.download_button("📥 Baixar PDF", pdf, "plano.pdf", "application/pdf")
        except: st.warning("Erro na geração do PDF.")

    with tab2:
        for msg in st.session_state.chat_history:
            st.chat_message(msg["role"]).write(msg["content"])
        if prompt := st.chat_input("Dúvida sobre o plano?"):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            
            ctx = f"Baseado no plano: {st.session_state.plano_final}. Responda: {prompt}"
            resp = model.generate_content(ctx).text
            
            st.session_state.chat_history.append({"role": "assistant", "content": resp})
            st.chat_message("assistant").write(resp)

# ROTEADOR
if st.session_state.pagina_atual == 'landing': pagina_landing()
elif st.session_state.pagina_atual == 'anamnese': pagina_anamnese()
elif st.session_state.pagina_atual == 'dashboard': pagina_dashboard()
