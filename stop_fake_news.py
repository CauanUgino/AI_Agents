import os
from dotenv import load_dotenv
from crewai import Agent, Task, Process, Crew, LLM
from crewai_tools import SerperDevTool
import streamlit as st
import time
import datetime

# Carregando variáveis de ambiente
load_dotenv()




OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# Instanciando o modelo LLM
llm = LLM(model='gpt-4o-mini', api_key=OPENAI_API_KEY)

# Instanciando a ferramenta de busca
search_tool = SerperDevTool()


st.set_page_config(page_title="Stop Fake News - Verificador", page_icon="📰", layout="centered")
st.markdown("""
    <style>
        .main {
            background-color: #f3f8f2;
            color: #0b3d0b;
        }
        .stButton > button {
            background-color: #2e7d32;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# SIDEBAR (DASHBOARD)
st.sidebar.title("📊 Verificações")
if 'historico' not in st.session_state:
    st.session_state['historico'] = []



# Informações do histórico
total_analises = len(st.session_state['historico'])
ultima_analise = st.session_state['historico'][-1]['tema'] if st.session_state['historico'] else "-"
ultima_data = st.session_state['historico'][-1]['data'] if st.session_state['historico'] else "-"
ultima_classificacao = st.session_state['historico'][-1]['classificacao'] if st.session_state['historico'] else "-"

st.sidebar.metric("Total de Análises", total_analises)
st.sidebar.metric("Último Tema", ultima_analise)
st.sidebar.metric("Data da Última", ultima_data)
st.sidebar.metric("Último Resultado", ultima_classificacao)

# Botão para limpar o histórico
if st.sidebar.button("🧹 Limpar histórico"):
    st.session_state['historico'] = []

# Garante que o histórico sempre exista como lista (ou esteja vazio)
historico = st.session_state.get('historico', [])


st.sidebar.markdown("---")
st.sidebar.markdown("Desenvolvido por **Cauan Ugino Filho**")
st.sidebar.caption("Aluno do Instituto Federal de Sergipe (IFS)")

st.markdown("---")
st.markdown("### 🤖 Informação sem verificação é desinformação")

st.title("📰 Stop Fake News")
st.subheader("Sistema de verificação de confiabilidade de notícias")


# Entrada do usuário
tema = st.text_input("Informe a Notícia:")
executar = st.button("Executar Verificação")

if executar and tema:
    with st.spinner("Analisando..."):
        # Aqui roda a verificação (simulação com sleep)
        time.sleep(60)  # simula tempo de análise
    st.success("Análise concluída!")
    with st.spinner ("Processando informação..."):
        time.sleep(25)
    st.success("Informações processadas...")
    
    # Agentes
    agente_buscador = Agent(
    role="Jornalista Investigativo",
    goal=f"Investigar sobre {tema} em fontes confiáveis como https://toolbox.google.com/factcheck/explorer/search/list:recent;hl=pt , https://lupa.uol.com.br/ ,  https://www.aosfatos.org/ ,  https://g1.globo.com/ , https://www.cnnbrasil.com.br/  , https://www.bbc.com/, etc.",
    backstory="Você é especialista em investigação de fake news com amplo acesso a ferramentas de busca.",
    tools=[search_tool],
    llm=llm,
    verbose=True,
    memory=True,
    allow_delegation=False
)

    # Agente linguístico
    agente_linguistico = Agent(
        role='Agente Linguístico',
        goal=("Avaliar o estilo textual do texto recebido, identificando excesso de adjetivos, "
            "linguagem alarmista e uso de clickbait."
            "Identificar o idioma e traduzir para o Português do Brasil."
            "aplica a avalição do estilo textual no texto"
        ),

        backstory='Você é um editor de textos experiente focado em melhorar a qualidade jornalística.',
        llm=llm,
        verbose=True,
        memory=False,
        allow_delegation=False
)

    agente_verificador = Agent(
        role='Verificador de Fatos',
        goal="Verificar os fatos presentes no texto final com fontes confiáveis como https://toolbox.google.com/factcheck/explorer/search/list:recent;hl=pt, https://lupa.uol.com.br/ e https://www.aosfatos.org/ ,  https://g1.globo.com/ , https://www.cnnbrasil.com.br/  , https://www.bbc.com/  ."
            "Mostre se a informação perguntada no {tema} é VERDADEIRA, FALSA ou PACIALMENTE VERDADEIRA",
        backstory=(
            "Você é um especialista em fact-checking, experiente em identificar notícias falsas "
            "e confirmar dados com fontes oficiais e confiáveis."
        ),
        tools=[search_tool],
        llm=llm,
        verbose=True,
        memory=False,
        allow_delegation=False
    )

    # Agente classificador de confiabilidade
    agente_classificador = Agent(
        role='Classificador de Confiabilidade',
        goal=(
            "Ler o texto revisado e o relatório de verificação de fatos. "
            "Aplicar regras heurísticas para decidir se a notícia é Confiável, Possivelmente Falsa ou Exige Verificação Adicional, "
            "com base nas fontes. "
            "Retornar uma resposta estruturada com dois campos:\n\n"
            "1) STATUS: <Confiável | Possivelmente Falsa | Exige Verificação Adicional>\n"
            "2) JUSTIFICATIVA: <texto explicando a decisão>\n"
            "Certifique-se de fornecer uma justificativa clara e objetiva com base nas evidências apresentadas."
        ),
        backstory=(
            "Você é um agente lógico que toma decisões com base em evidências fornecidas pelos outros agentes. "
            "Utiliza regras heurísticas e simbólicas para garantir uma classificação confiável."
        ),
        llm=llm,
        verbose=False,
        memory=False,
        allow_delegation=False
    )


    # Tarefas da primeira etapa
    tarefa_buscador = Task(
        description=f'Pesquisar notícias confiáveis sobre {tema} nos sites como https://www.bbc.com/ , https://www.bbc.com/portuguese/topics/cz74k717pw5t , https://www.bbc.com/portuguese/topics/cz74k717pw5t , https://g1.globo.com/https://g1.globo.com/ e criar um relatório com fatos e links.',
        expected_output='Relatório com data, fontes e links.',
        agent=agente_buscador,
        output_file='relatorio_investigativo.md'
    )

    tarefa_linguistica = Task(
        description='Analisar o texto jornalístico e avaliar o estilo textual conforme critérios definidos.',
        expected_output=(
            "Texto jornalístico revisado e editado, com linguagem adequada, "
            "sem excesso de adjetivos, sem tom alarmista e sem clickbait, "
            "traduzido para o Português do Brasil, se necessário."
        ),
        agent=agente_linguistico,
        input='relatorio_investigativo.md',
        output_file='relatorio_linguistico.md'
    )

    # Tem erro aqui na parte dizer qual e verdade, duvidoso ou fake
    tarefa_verificacao = Task(
        description="Verificar os fatos do texto editado com fontes em sites como https://toolbox.google.com/factcheck/explorer/search/list:recent;hl=pt , https://lupa.uol.com.br/, Aos https://www.aosfatos.org/ . Gerar relatório de veracidade.",
        expected_output="Exibir as noticias encontradas, e abaixo exibir a fonte e link"
                        "Traduzir tudo para o Português do Brasil"
                        "Exiba o resultado da verificação da noticia informada no tema, dizendo se é VERDADEIRA, FALSA ou PACIALMENTE VERDADEIRA"
                        "Exiba a noticia das fontes encontradas",
        agent=agente_verificador,
        input='relatorio_linguistico.md',
        output_file='relatorio_verificacao.md'
    )

    equipe_inicial = Crew(
        agents=[agente_buscador, agente_linguistico, agente_verificador],
        tasks=[tarefa_buscador, tarefa_linguistica, tarefa_verificacao],
        process=Process.sequential,
        llm=llm
    )

    equipe_inicial.kickoff(inputs={'tema': tema})

    with open("relatorio_linguistico.md", "r", encoding="utf-8") as f1, open("relatorio_verificacao.md", "r", encoding="utf-8") as f2:
        texto_final = "# Texto Jornalístico Revisado\n\n" + f1.read() + "\n\n# Relatório de Verificação de Fatos\n\n" + f2.read()

    with open("entrada_classificacao.md", "w", encoding="utf-8") as f_out:
        f_out.write(texto_final)

    # Tarefa de classificação
    tarefa_classificacao = Task(
        description=(
            "Ler o texto revisado e o relatório de verificação de fatos. "
            "Aplicar regras heurísticas para decidir se a notícia é confiável, possivelmente falsa ou exige verificação adicional. "
            "Aplique acima da noticia um nome que confirme tipo: Confiável, possivelmente falsa"
            "Comece o parecer com: STATUS: <classificação> e em seguida: "
            "JUSTIFICATIVA: <explicação detalhada>."

        ),
        expected_output=(
            "Classificação final da notícia: Confiável, possivelmente falsa, com justificativas."
        ),
        agent=agente_classificador,
        input='entrada_classificacao.md',
        output_file='Resultado_final.md'
    )


    equipe_final = Crew(
        agents=[agente_classificador],
        tasks=[tarefa_classificacao],
        process=Process.sequential,
        llm=llm
    )

    equipe_final.kickoff()

    with open("relatorio_verificacao.md", "r", encoding="utf-8") as f:
        st.markdown("### 🔍 Relatório de Verificação de Fatos")
        st.markdown(f.read())

    with open("Resultado_final.md", "r", encoding="utf-8") as f:
        st.markdown("### ✅ Parecer Final")
        st.markdown(f.read())


       # === Salvando no histórico da sessão ===
    if "Confiável" in 'parecer_final':
        classificacao = "Confiável"
    elif "Possivelmente Falsa" in 'parecer_final':
        classificacao = "Possivelmente Falsa"
    else:
        classificacao = "Exige Verificação Adicional"

    st.session_state['historico'].append({
        "tema": tema,
        "data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
        "classificacao": classificacao
    })


    



    
elif executar:
    st.warning("Por favor, insira um tema para iniciar a verificação.")
