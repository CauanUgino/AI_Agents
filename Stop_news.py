import os
from crewai import Agent, Task, Process, Crew, LLM
from dotenv import load_dotenv


# Carregar variáveis de ambiente
load_dotenv()


OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# Inicializando o modelo de LLM
#llm = LLM(model="ollama/llama3.2", base_url="http://localhost:11434")
llm = LLM(model='gpt-4o-mini', api_key=OPENAI_API_KEY)


tema= input("Informe o tema da pesquisa: ")

# Criando o agente de pesquisa de dados climáticos
agente_buscador = Agent(
    role='jornalista investigativo',
    goal='Pesquisar noticias atualizadas sobre {tema} em sites confiaveis como BBC, CNN, G1, Folha, Estadão, etc. '
         'E gerar um relatótrio com os principais fatos, impactos e contextos. ',    

     backstory='você é um jornalista investigativo com experiência em pesquisa de dados e análise de informações. '
               'Você é especialista em encontrar informações relevantes e confiáveis sobre diversos temas, '
               'e tem acesso a ferramentas de busca avançadas para ajudá-lo em sua investigação.',
    verbose=True,
    memory=True,
    llm=llm,
    tools=['serper'],
    allow_delegation= False
)

tarefa_busca = Task(
    description= f"Pesquisar noticias atualizadas sobre {tema} em sites confiaveis como BBC, CNN, G1, Folha, Estadão, etc. "
                     'E gerar um relatótrio com os principais fatos, impactos e contextos. ',
     expected_output= 'Um relatório claro com data, fontes e links das noticias e as informações encontradas.',
     agent=agente_buscador,
     output_file="relatorio_investigativo.md",
)

equipe = Crew(
    agents=[agente_buscador],
    tasks=[tarefa_busca],
    process=Process.sequential,
    llm=llm
)


resultados = equipe.kickoff(inputs={'tema': tema})
print("Resultados da Pesquisa:\n", resultados)