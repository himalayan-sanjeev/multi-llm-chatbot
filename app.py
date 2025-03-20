import streamlit as st
import google.generativeai as genai  # Gemini
import openai  # ChatGPT
import anthropic  # Claude
import requests


# Load API Keys from secrets
api_keys = st.secrets["api_keys"]
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"  # DeepSeek API URL

# Initialize Chat History in Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "Gemini (Google)"

# UI: Chat Title & Sidebar
st.title("Himalayan Multi-LLM Chatbot")
st.sidebar.header("⚙️ Settings")

# Model Selection
selected_model = st.sidebar.selectbox("Choose a Model:", 
                                      ["Gemini (Google)", "OpenAI (ChatGPT)","Claude (Anthropic)", "DeepSeek"],
                                      index=["Gemini (Google)", "OpenAI (ChatGPT)", "Claude (Anthropic)", "DeepSeek"].index(st.session_state.selected_model))

# Store selected model in session state
st.session_state.selected_model = selected_model

# Chat Interface
st.write("### 💬 Chat Thread")
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User Input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Display User Message
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # AI Response Placeholder
    with st.chat_message("assistant"):
        response_placeholder = st.empty()

    # Process the response based on selected model
    if selected_model == "OpenAI (ChatGPT)":
        openai.api_key = api_keys["openai"]
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.chat_history]
        )
        ai_response = response["choices"][0]["message"]["content"]

    elif selected_model == "Gemini (Google)":
        genai.configure(api_key=api_keys["gemini"])
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(user_input)
        ai_response = response.text

    elif selected_model == "Claude (Anthropic)":
        client = anthropic.Anthropic(api_key=api_keys["anthropic"])
        response = client.messages.create(
            model="claude-3-opus-20240229",
            messages=[{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.chat_history]
        )
        ai_response = response["content"]

    elif selected_model == "DeepSeek":
        headers = {
            "Authorization": f"Bearer {api_keys['deepseek']}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "deepseek-chat",
            "messages": [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.chat_history],
            "temperature": 0.7
        }

        response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)
        
        if response.status_code == 200:
            ai_response = response.json()["choices"][0]["message"]["content"]
        else:
            ai_response = f"❌ DeepSeek API Error: {response.json()}"

    # Display AI Response
    response_placeholder.write(ai_response)
    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})

# Button to Clear Chat
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()
