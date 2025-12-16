# agentes.py
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions
import time
from fpdf import FPDF
import streamlit as st
from prompts import PROMPT_PERSONAL, PROMPT_FISIO, PROMPT_NUTRI, PROMPT_MEDICO_GERAL

def configurar_google_api():
    api_key = None
    try:
        if "google" in st.secrets and "api_key" in st.secrets["google"]:
            api_key = st.secrets["google"]["api_key"]
        elif "GOOGLE_API_KEY" in st.secrets:
            api_key = st.secrets["GOOGLE_API_KEY"]
    except:
        pass
    
    if api_key:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel(model_name="gemini-2.5-flash-lite",
                                     generation_config={"temperature": 0.7, "max_output_tokens": 8192})
    return None

def gerar_pdf(texto_plano):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Plano de Saude Holistica - IA", ln=1, align='C')
    pdf.ln(10)
    try:
        texto_limpo = texto_plano.encode('latin-1', 'replace').decode('latin-1')
    except:
        texto_limpo = texto_plano
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 6, txt=texto_limpo)
    return pdf.output(dest='S').encode('latin-1')

def chamar_especialista(model, persona_prompt, historico_conversa, tarefa_atual, status_container):
    prompt_completo = f"""
    {persona_prompt}
    --- HISTÓRICO ---
    {historico_conversa}
    --- TAREFA ---
    {tarefa_atual}
    Responda começando com 'ok' se estiver tudo certo, ou proponha a mudança.
    """
    max_tentativas = 3
    for tentativa in range(max_tentativas):
        try:
            response = model.generate_content(prompt_completo)
            return response.text.strip()
        except google_exceptions.TooManyRequests:
            status_container.warning(f"Aguardando API... ({tentativa+1}/{max_tentativas})")
            time.sleep(20)
        except Exception as e:
            status_container.error(f"Erro: {e}")
            raise e
    return "ERRO: Sem resposta."

def simular_agentes(d, model):
    desc_user = f"""
    PERFIL: {d['nome']}, {d['idade']} anos, {d['sexo']}. CORPO: {d['peso']}kg, {d['altura']}cm.
    OBJETIVO: {d['objetivo_detalhado']}
    ROTINA: "{d['rotina_texto']}"
    TREINO: {d['dias_treino']}x/sem, {d['local_treino']}, {d['tempo_treino']}min.
    SAUDE: {d['lesoes']}, {d['saude_geral']}.
    NUTRI: Cozinha? {d['cozinha']}, {d['refeicoes_dia']} ref/dia, Orçamento {d['orcamento']}, Água {d['agua_atual']}L.
    """
    
    consenso_atingido = False
    historico = f"Paciente: {desc_user}\n"
    plano = "Nenhum plano ainda."
    ciclo = 0
    max_ciclos = 2

    with st.status("Reunião do Conselho Multidisciplinar...", expanded=True) as status:
        while not consenso_atingido and ciclo < max_ciclos:
            ciclo += 1
            status.write(f"--- 🔄 Ciclo {ciclo} ---")
            oks = []

            # Personal
            status.write("🏋️ Personal Trainer...")
            resp = chamar_especialista(model, PROMPT_PERSONAL, historico, f"Criar/ajustar plano. Atual: {plano}", status)
            plano = resp; historico += f"Personal: {resp}\n"; oks.append(resp.lower().startswith('ok'))
            
            # Fisio
            status.write("🩺 Fisioterapeuta...")
            resp = chamar_especialista(model, PROMPT_FISIO, historico, f"Validar segurança. Atual: {plano}", status)
            plano = resp; historico += f"Fisio: {resp}\n"; oks.append(resp.lower().startswith('ok'))

            # Nutri
            status.write("🍎 Nutricionista...")
            resp = chamar_especialista(model, PROMPT_NUTRI, historico, f"Inserir Dieta Detalhada. Atual: {plano}", status)
            plano = resp; historico += f"Nutri: {resp}\n"; oks.append(resp.lower().startswith('ok'))

            # Coach
            status.write("🧘 Coach...")
            resp = chamar_especialista(model, PROMPT_MEDICO_GERAL, historico, f"Formatar Final. Atual: {plano}", status)
            plano = resp; historico += f"Coach: {resp}\n"; oks.append(resp.lower().startswith('ok'))

            if all(oks):
                consenso_atingido = True
                status.update(label="Plano Pronto!", state="complete", expanded=False)
    
    return plano
