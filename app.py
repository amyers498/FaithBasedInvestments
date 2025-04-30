import streamlit as st
import requests
import json
from config import GROK_API_KEY

# Streamlit page config
st.set_page_config(page_title="FaithFin Investor Bot", page_icon="🙏", layout="centered")

# Custom CSS for dark mode with a sleek, faith-inspired look
st.markdown("""
    <style>
    .main {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #4A90E2;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        border: none;
        box-shadow: 0 0 10px rgba(74, 144, 226, 0.5);
    }
    .stButton>button:hover {
        background-color: #357ABD;
        box-shadow: 0 0 15px rgba(74, 144, 226, 0.8);
    }
    .stTextInput>div>input {
        background-color: #2C2C2C;
        color: white;
        border-radius: 8px;
        border: 1px solid #555;
        padding: 10px;
    }
    .stSelectbox>div {
        background-color: #2C2C2C;
        color: white;
        border-radius: 8px;
        border: 1px solid #555;
    }
    .chat-container {
        background-color: #2C2C2C;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.3);
        margin-top: 20px;
    }
    .user-message {
        background-color: #4A90E2;
        color: white;
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
        box-shadow: 0 0 5px rgba(74, 144, 226, 0.5);
    }
    .grok-message {
        background-color: #2ECC71;
        color: white;
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
        box-shadow: 0 0 5px rgba(46, 204, 113, 0.5);
    }
    .header {
        text-align: center;
        color: #E0E0E0;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 10px;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
    }
    .subheader {
        text-align: center;
        color: #A0A0A0;
        font-size: 1.2em;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Header
st.markdown('<div class="header">FaithFin Investor Bot</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Align Your Investments with Your Faith</div>', unsafe_allow_html=True)

# Religion selection
religion = st.selectbox("Select Your Religion", ["Christian", "Muslim", "Jewish"], help="Choose your faith for tailored investment advice.")

# Question input
question = st.text_input("Ask About Investments", placeholder="e.g., Is Tesla Christian-compliant? What can I invest in as a Muslim?")

# Submit button
if st.button("Ask FaithFin"):
    if question.strip() == "":
        st.error("Please enter a question.")
    else:
        # Prepare Grok API request
        headers = {
            "Authorization": f"Bearer {GROK_API_KEY}",
            "Content-Type": "application/json"
        }
        faith_context = {
            "Christian": "You are an expert in Christian-aligned investing, ensuring investments avoid companies involved in alcohol, gambling, abortion, or other activities contrary to Christian values, per Catholic Investment Guidelines.",
            "Muslim": "You are an expert in Sharia-compliant investing, ensuring investments avoid interest (riba), alcohol, pork, gambling, or other haram activities, per AAOIFI standards.",
            "Jewish": "You are an expert in Jewish ethical investing, prioritizing ESG factors and avoiding exploitation or unethical businesses, per Jewish ESG principles."
        }
        system_prompt = faith_context[religion]
        user_prompt = question

        payload = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "model": "grok-3-latest",
            "stream": False,
            "temperature": 0
        }

        try:
            # Call Grok API
            response = requests.post("https://api.x.ai/v1/chat/completions", headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            answer = result.get("choices", [{}])[0].get("message", {}).get("content", "Sorry, I couldn't process your request.")

            # Update chat history
            st.session_state.chat_history.append({"question": question, "answer": answer})

        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to Grok API: {str(e)}")
            st.session_state.chat_history.append({"question": question, "answer": "Error: Could not connect to FaithFin AI."})

# Display chat history
if st.session_state.chat_history:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    st.write("**Conversation History**")
    for chat in st.session_state.chat_history:
        st.markdown(f'<div class="user-message"><strong>You:</strong> {chat["question"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="grok-message"><strong>FaithFin:</strong> {chat["answer"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)