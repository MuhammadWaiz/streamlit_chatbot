import streamlit as st
import time
from google import genai

def authenticate(api_key):
    """Authenticate the user by testing the API key."""
    try:
        client = genai.Client(api_key=api_key)
        # Simple test request to check API validity
        client.models.generate_content(model="gemini-2.0-flash", contents="Hello")
        return client
    except Exception:
        st.error("❌ Invalid API Key. Please enter a valid key.")
        return None

# Streamlit UI
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")
st.markdown("""
    <style>
        body {
            background-color: #000000;
            color: #ffffff;
        }
        .big-title {
            font-size: 40px;
            font-weight: bold;
            text-align: center;
            color: #FFD700;
            margin-bottom: 20px;
        }
        .chat-box {
            background-color: #444444;
            padding: 15px;
            border-radius: 10px;
            color: #ffffff; /* Changed chatbot reply text to white */
            font-size: 18px;
            font-weight: bold;
            margin-top: 10px;
            border-left: 5px solid #32CD32;
            box-shadow: 2px 2px 10px rgba(255, 215, 0, 0.3);
            animation: fadeIn 0.5s ease-in-out;
        }
        .input-container {
            max-width: 600px;
            margin: 20px auto;
            padding: 15px;
            background: #1a1a1a;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(255, 215, 0, 0.3);
        }
        .user-input {
            margin-top: 20px;
            padding: 12px;
            border-radius: 8px;
            background-color: #222222;
            color: #ffffff;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-title">🤖 AI Chatbot</p>', unsafe_allow_html=True)

# API Key Input
api_key = st.text_input("🔑 Enter your API Key to continue:", type="password")
client = None

if api_key:
    client = authenticate(api_key)  # Check API Key Validity

if client:
    st.success("✅ Authentication successful! Start chatting below.")

    # Chat input section

    user_input = st.text_input("💬 Ask me anything:", key="user_input", help="Type your message here")

    if user_input:
        with st.spinner("Thinking..."):
            response = client.models.generate_content(
                model="gemini-2.0-flash", contents=user_input
            )

        # Typing effect for chatbot response
        bot_response = ""
        response_container = st.empty()
        for char in response.text:
            bot_response += char
            time.sleep(0.02)  # Typing delay effect
            response_container.markdown(f'<div class="chat-box">🤖 <b>Chatbot:</b> {bot_response}</div>', unsafe_allow_html=True)

else:
    st.warning("⚠️ Please enter a valid API Key to access the chatbot.")
