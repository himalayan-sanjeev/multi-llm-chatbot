# 🤖 Multi-LLM Chatbot (ChatGPT, Gemini, Claude, DeepSeek)

An interactive **Streamlit** web app that allows users to:
- **Chat with multiple AI models** (ChatGPT, Gemini, Claude, DeepSeek) 🔥
- **Dynamically switch between models** using a dropdown menu 🎛️
- **Maintain multi-turn conversations** just like ChatGPT 🗨️
- **Supports API Key Configuration** for secure access 🔑

---
## 🖥 Running the App

To start the **Multi-LLM Chatbot**, follow these steps:

###  Clone the Repository
```bash
git clone https://github.com/himalayan-sanjeev/multi-llm-chatbot
cd multi-llm-chatbot
```

###  Install dependencies
```bash
pip install -r requirements.txt
```

###  Run the app
```bash
streamlit run app.py
```
This will open the web app in your browser. 

#### Set Up Secrets for different LLM apis

Create a ```.streamlit/secrets.toml``` file and add your API Keys:

```bash
[api_keys]
gemini = "your-gemini-api-key"
openai = "your-openai-api-key"
anthropic = "your-anthropic-api-key" 
deepseek = "your-deepseek-api-key"
```