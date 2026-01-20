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
# Deep Blue Background + Custom CSS
# -------------------------------
st.markdown(
    """
    <style>
    body {
        background-color: #1e3a8a;  /* deep blue */
        color: white;  /* text in white */
    }
    div.stButton > button {
        background-color: #6c5ce7;  /* purple button */
        color: white;
        height: 3em;
        width: 100%;
        border-radius: 10px;
        font-size: 16px;
    }
    div.stButton > button:hover {
        background-color: #a29bfe;  /* lighter purple on hover */
        color: white;
    }
    .stTextArea>label {
        font-weight: bold;
        color: white;
    }
    .stMarkdown {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------
# App Header
# -------------------------------
st.image("https://cdn-icons-png.flaticon.com/512/4712/4712307.png", width=80)
st.title("🤖 AI Study Assistant")
st.markdown(
    "Ask questions and get answers powered by OpenAI GPT models! "
    "Type your prompt and see the AI in action."
)
st.markdown("---")

# -------------------------------
# Load API Key
# -------------------------------
api_key = os.getenv("OPENAI_API_KEY")

# Optional fallback if API key not found
if not api_key:
    st.warning("OpenAI API key not found in secrets. Please enter it below:")
    api_key = st.text_input("Enter your OpenAI API Key", type="password")

# Initialize OpenAI client
if api_key:
    client = OpenAI(api_key=api_key)

# -------------------------------
# Layout: Input and Output Columns
# -------------------------------
col1, col2 = st.columns([1, 1])

with col1:
    with st.container():
        st.markdown("### 💬 Your Input")
        user_prompt = st.text_area(
            "Type your question or prompt here:",
            height=200
        )

with col2:
    with st.container():
        st.markdown("### 🤖 AI Response")
        # Placeholder for AI output
        ai_response_box = st.empty()

# -------------------------------
# Generate Response
# -------------------------------
if st.button("Get Answer"):
    if not user_prompt:
        st.error("Please enter a prompt first!")
    elif not api_key:
        st.error("API key required to connect to OpenAI.")
    else:
        with st.spinner("Generating response..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful AI assistant."},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=200
                )
                answer = response.choices[0].message.content.strip()
                ai_response_box.success(answer)
            except Exception as e:
                ai_response_box.error(f"Error connecting to OpenAI: {e}")

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown(
    "💡 **Tip:** Your OpenAI API key is kept secure using Streamlit Secrets. "
    "If not provided, you can enter it manually above. "
    "Enjoy your AI Study Assistant!"
)
