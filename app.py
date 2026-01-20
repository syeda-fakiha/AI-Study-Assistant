import streamlit as st
from openai import OpenAI

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="🤖",
    layout="centered"
)

MAX_CHARS = 400

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp { background-color: #0A3D62; font-family: 'Segoe UI', sans-serif; }
header, footer {visibility: hidden;}

.main-title {text-align: center; font-size: 40px; font-weight: bold; color: #F8EFBA;}
.subtitle {text-align: center; font-size: 18px; color: #DFF9FB; margin-bottom: 25px;}
.ask-label {font-size: 24px; font-weight: bold; color: #A8E6CF;}
.stTextInput input {background-color: #1B4F72; color: #E8F8F5; border-radius: 12px; border: 2px solid #74B9FF; padding: 14px; font-size: 18px;}
.stButton button {background-color: #74B9FF; color: black; font-size: 17px; font-weight: bold; border-radius: 12px; width: 100%;}
.chat-box {background-color: #1B4F72; padding: 18px; border-radius: 14px; margin-top: 15px; color: #ECF0F1;}
.user-text {color: #F9E79F; font-weight: bold;}
.ai-text {color: #D6EAF8;}
.footer-note {text-align: center; color: #D6EAF8; font-size: 14px; margin-top: 40px; opacity: 0.8;}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "chats" not in st.session_state:
    st.session_state.chats = []  # list of conversations
if "active_chat" not in st.session_state:
    st.session_state.active_chat = []

# ---------------- OPENAI CLIENT ----------------
# Try getting API key from Secrets
api_key = st.secrets.get("project_API_KEY")

# If no key in Secrets, allow manual input
if not api_key:
    api_key = st.text_input("Enter your OpenAI API Key", type="password")

# Only initialize client if key exists
client = None
if api_key:
    try:
        client = OpenAI(api_key=api_key)
    except Exception as e:
        st.error(f"Error initializing OpenAI client: {str(e)}")
else:
    st.warning("⚠️ OpenAI API Key missing! Please add it in Streamlit Secrets or enter manually.")

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## 🧾 Chat History")
    
    if st.session_state.chats:
        for idx, conv in enumerate(st.session_state.chats[::-1]):
            # show first line as label
            label = conv[0][0] if conv else f"Chat {len(st.session_state.chats)-idx}"
            if st.button(label[:35], key=f"chat_{idx}"):
                st.session_state.active_chat = conv.copy()
    else:
        st.info("No chats yet")
    
    if st.button("🆕 New Chat"):
        st.session_state.active_chat = []

# ---------------- MAIN UI ----------------
st.markdown('<div class="main-title">🤖 AI Study Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Ask questions and get AI-powered help</div>', unsafe_allow_html=True)

# ---------------- INPUT + PROCESS ----------------
with st.form("question_form", clear_on_submit=True):
    st.markdown('<div class="ask-label">Ask a Question</div>', unsafe_allow_html=True)
    question = st.text_input(
        "Your Question",  # required for accessibility
        placeholder="Type your question and press Enter...",
        label_visibility="collapsed"
    )
    submitted = st.form_submit_button("Ask AI")

    if submitted:
        if not question.strip():
            st.warning("Please enter a question before submitting.")
        elif len(question) > MAX_CHARS:
            st.warning(f"Question too long. Limit is {MAX_CHARS} characters.")
        elif not client:
            st.error("Cannot connect to AI: OpenAI API key missing or invalid.")
        else:
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful academic study assistant."},
                        {"role": "user", "content": question}
                    ]
                )
                answer = response.choices[0].message.content
                st.session_state.active_chat.append((question, answer))

                # Save to chats if not already saved
                if st.session_state.active_chat not in st.session_state.chats:
                    st.session_state.chats.append(st.session_state.active_chat.copy())

            except Exception as e:
                # Handle quota errors nicely
                if "insufficient_quota" in str(e):
                    st.error("⚠️ Your OpenAI API key has no remaining quota. Please update it.")
                else:
                    st.error(f"Error connecting to AI: {str(e)}")

# ---------------- DISPLAY CONVERSATION ----------------
if st.session_state.active_chat:
    st.markdown("### 💬 Conversation")
    for q, a in st.session_state.active_chat[::-1]:
        st.markdown(f"""
        <div class="chat-box">
            <div class="user-text">You:</div>
            {q}
            <br><br>
            <div class="ai-text"><b>AI:</b> {a}</div>
        </div>
        """, unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer-note">
⚠️ I can make mistakes. Please verify important information.
</div>
""", unsafe_allow_html=True)
