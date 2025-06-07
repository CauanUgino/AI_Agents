# 🛡️ Stop Fake News

**Stop Fake News** é um sistema inteligente de verificação de notícias com foco em combater a desinformação de forma automatizada, transparente e acessível. Utilizando **agentes inteligentes com LLMs**, o sistema analisa conteúdos, classifica sua confiabilidade, gera relatórios explicativos e ainda fornece QR Codes para consulta das fontes.

---

## 🚀 Funcionalidades

✅ **Verificação Automatizada de Notícias**  
Sistema com agentes inteligentes que analisam o conteúdo suspeito e executam checagem com base em fontes confiáveis.

🔍 **Classificação de Confiabilidade**  
O resultado da análise classifica a notícia como:
- ✅ **Confiável**
- ⚠️ **Parcialmente confiável**
- ❌ **Falsa**

🧠 **Geração de Relatórios Explicativos**  
Cada verificação vem acompanhada de uma justificativa detalhada do parecer final.

🌐 **QR Code com Fontes**  
Geração de QR Code que leva diretamente para os links utilizados durante a verificação.

📚 **Histórico de Sessão**  
As últimas verificações realizadas ficam salvas temporariamente e podem ser acessadas ao longo do uso.

💾 **Persistência em Banco de Dados (MySQL)**  
Cada verificação é salva no banco com:
- Tema da notícia
- Texto original
- Texto verificado
- Parecer final
- QR Code
- Data/hora

🎨 **Interface Responsiva com Streamlit**  
Interface limpa, moderna e intuitiva para qualquer tipo de usuário.

---

## 🧠 Arquitetura Tecnológica

- **Frontend:** [Streamlit](https://streamlit.io/)  
- **Backend:** Python 3.10+ com agentes LLM (via [CrewAI](https://docs.crewai.com))  
- **Banco de Dados:** MySQL  
- **APIs e Ferramentas:** Serper API, QR Code, OpenAI, etc.  

---

## 📦 Como Executar o Projeto Localmente

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/stop-fake-news.git
cd stop-fake-news

# Crie o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure suas variáveis de ambiente (exemplo: .env)
# OPENAI_API_KEY=...
# SERPER_API_KEY=...
# DB_HOST=localhost
# DB_USER=root
# DB_PASSWORD=123456
# DB_NAME=stop_fake_news

# Execute a aplicação
streamlit run app.py
