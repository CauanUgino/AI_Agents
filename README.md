# Jornalista Investigativo com IA (CrewAI + GPT-4o-mini + Serper)

Este projeto utiliza a biblioteca [CrewAI](https://docs.crewai.com) e a API Serper para criar um agente de **jornalismo investigativo automatizado** que busca notícias atuais sobre um tema específico, acessando fontes confiáveis como **BBC, CNN, G1, Folha, Estadão**, entre outras.  
O resultado é um relatório técnico com **datas, fontes e links diretos**.

---

## Tecnologias Utilizadas

- [Python 3.10+](https://www.python.org/)
- [CrewAI](https://github.com/joaomdmoura/crewAI)
- [OpenAI GPT-4o-mini](https://openai.com/)
- [Serper API (Google Search API)](https://serper.dev/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## Como Executar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/jornalista-ia.git
cd jornalista-ia

2. Crie um ambiente virtual:
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

3. Instale as dependências:
pip install -r requirements.txt

4. Configure as variáveis de ambiente:
OPENAI_API_KEY=sua-chave-da-openai
SERPER_API_KEY=sua-chave-da-serper

5. Execute o programa.
