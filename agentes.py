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
    class PDF(FPDF):
        def header(self):
            # Logo ou Título
            self.set_font('Arial', 'B', 16)
            self.cell(0, 10, 'Plano de Saúde Holística - IA', 0, 1, 'C')
            self.ln(5)
            
        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Processar texto para simular formatação Markdown básica (Negrito)
    # FPDF padrão não suporta Markdown nativo, vamos fazer algo simples
    # ou apenas melhorar a fonte e espaçamento.
    
    pdf.set_font("Arial", size=11)
    
    # Tratamento básico de caracteres
    try:
        linhas = texto_plano.split('\n')
        for linha in linhas:
            linha = linha.encode('latin-1', 'replace').decode('latin-1')
            
            # Títulos (detectados por ## ou algo assim no markdown original)
            if linha.strip().startswith('##'):
                pdf.ln(5)
                pdf.set_font("Arial", 'B', 14)
                pdf.multi_cell(0, 8, txt=linha.replace('#', '').strip())
                pdf.set_font("Arial", size=11)
            # Subtítulos ou negrito simulado
            elif linha.strip().startswith('**'):
                pdf.ln(2)
                pdf.set_font("Arial", 'B', 11)
                pdf.multi_cell(0, 6, txt=linha.replace('*', '').strip())
                pdf.set_font("Arial", size=11)
            else:
                pdf.multi_cell(0, 6, txt=linha)
                
    except Exception as e:
        pdf.multi_cell(0, 6, txt=f"Erro ao formatar PDF: {e}")
        
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

    # Container para o debate
    debate_container = st.container()
    
    with debate_container:
        st.subheader("💬 Reunião do Conselho")
        
        while not consenso_atingido and ciclo < max_ciclos:
            ciclo += 1
            st.markdown(f"**--- 🔄 Ciclo {ciclo} ---**")
            oks = []

            # Agentes e seus ícones/nomes
            agentes = [
                ("Personal Trainer", "🏋️", PROMPT_PERSONAL, "Criar/ajustar plano."),
                ("Fisioterapeuta", "🩺", PROMPT_FISIO, "Validar segurança."),
                ("Nutricionista", "🍎", PROMPT_NUTRI, "Inserir Dieta Detalhada."),
                ("Coach de Saúde", "🧘", PROMPT_MEDICO_GERAL, "Formatar Final.")
            ]

            for nome, icon, prompt_persona, tarefa_base in agentes:
                # Mostra que o agente está pensando
                with st.spinner(f"{nome} está analisando..."):
                    tarefa = f"{tarefa_base} Atual: {plano}" if ciclo > 1 or nome != "Personal Trainer" else tarefa_base
                    resp = chamar_especialista(model, prompt_persona, historico, tarefa, st.empty())
                    
                    # Atualiza estado do plano
                    plano = resp if "Coach" in nome or ciclo > 0 else (plano + "\n" + resp) 
                    # Nota: A lógica de concatenação original estava sobrescrevendo 'plano = resp'.
                    # Vamos manter a lógica original de sobrescrever para simplificar, mas o ideal seria evoluir.
                    plano = resp 
                    historico += f"{nome}: {resp}\n"
                    oks.append(resp.lower().strip().startswith('ok'))
                
                # Exibe a fala do agente na UI
                with st.chat_message(nome, avatar=icon):
                    st.write(f"**{nome}**: {resp[:300]}..." if len(resp) > 300 else f"**{nome}**: {resp}")
                    with st.expander("Ver detalhes"):
                        st.markdown(resp)
                    time.sleep(1) # Pequena pausa dramática para leitura

            if all(oks):
                consenso_atingido = True
                st.success("✅ Conselho chegou a um consenso!")
                time.sleep(1.5)
    
    return plano
