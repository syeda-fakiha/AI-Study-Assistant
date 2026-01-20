# app.py
import streamlit as st
import os
from openai import OpenAI

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------
# Global CSS (Blue background + cards)
# -------------------------------
st.markdown("""
<style>
.stApp {
    background-color: #1e3a8a;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #172554;
    color: white;
}

/* White cards */
.card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    color: #1f2937;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
}

/* Chat bubbles */
.user-bubble {
    background-color: #dbeafe;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 10px;
}

.ai-bubble {
    background-color: #ede9fe;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 10px;
}

/* Button */
div.stButton > button {
    background-color: #6c5ce7;
    color: white;
    height: 3em;
    width: 100%;
    border-radius: 10px;
    font-size: 16px;
    border: none;
}

div.stButton > button:hover {
    background-color: #a29bfe;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Sidebar
# -------------------------------
with st.sidebar:
    st.markdown("## 🤖 AI Study Assistant")
    st.markdown(
        """
        **Features**
        - Ask academic questions  
        - Get AI-generated answers  
        - Powered by OpenAI  

        **How to use**
        1. Enter your question  
        2. Click **Get Answer**  
        3. Read AI response  
        """
    )

# -------------------------------
# Header
# -------------------------------
st.markdown("<h1 style='color:white;'>🤖 AI Study Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:white;'>Your smart study companion</p>", unsafe_allow_html=True)
st.markdown("---")

# -------------------------------
# API Key
# -------------------------------
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.warning("API key not found in secrets.")
    api_key = st.text_input("Enter OpenAI API Key", type="password")

if api_key:
    client = OpenAI(api_key=api_key)

# -------------------------------
# Chat History
# -------------------------------
if "chat" not in st.session_state:
    st.session_state.chat = []

# -------------------------------
# Layout
# -------------------------------
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 💬 Ask a Question")
    user_input = st.text_area("Type here:", height=150)
    send = st.button("Get Answer")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🤖 Conversation")

    for msg in st.session_state.chat:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-bubble'><b>You:</b> {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='ai-bubble'><b>AI:</b> {msg['content']}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# Generate Response
# -------------------------------
if send:
    if not user_input:
        st.error("Please enter a question.")
    elif not api_key:
        st.error("API key required.")
    else:
        st.session_state.chat.append({"role": "user", "content": user_input})

        with st.spinner("AI is thinking..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful study assistant."},
                        *st.session_state.chat
                    ],
                    temperature=0.7,
                    max_tokens=250
                )

                answer = response.choices[0].message.content.strip()
                st.session_state.chat.append({"role": "assistant", "content": answer})
                st.rerun()

            except Exception as e:
                st.error(e)

# -------------------------------
# Footer
# -------------------------------
st.markdown(
    "<p style='color:white; text-align:center;'>© 2026 AI Study Assistant | Streamlit + OpenAI</p>",
    unsafe_allow_html=True
)
