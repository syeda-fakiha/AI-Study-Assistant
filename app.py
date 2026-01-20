import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="🤖",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

/* Main app background */
.stApp {
    background-color: #0A3D62;
    font-family: 'Segoe UI', sans-serif;
}

/* Remove default white header space */
header {visibility: hidden;}
footer {visibility: hidden;}

/* Title */
.main-title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: #F8EFBA;
    margin-bottom: 10px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    font-size: 18px;
    color: #DFF9FB;
    margin-bottom: 30px;
}

/* Ask Question Label */
.ask-label {
    font-size: 22px;
    font-weight: bold;
    color: #A8E6CF;
    margin-bottom: 5px;
}

/* Input box */
.stTextInput input {
    background-color: #1B4F72;
    color: #E8F8F5;
    border-radius: 12px;
    border: 2px solid #74B9FF;
    padding: 14px;
    font-size: 18px;
}

/* Placeholder */
.stTextInput input::placeholder {
    color: #C7ECEE;
}

/* Button */
.stButton button {
    background-color: #74B9FF;
    color: black;
    font-size: 17px;
    font-weight: bold;
    border-radius: 12px;
    padding: 12px 20px;
    width: 100%;
}

.stButton button:hover {
    background-color: #0984E3;
    color: white;
}

/* Conversation box */
.chat-box {
    background-color: #1B4F72;
    padding: 20px;
    border-radius: 15px;
    margin-top: 20px;
    color: #ECF0F1;
    font-size: 16px;
}

/* User text */
.user-text {
    color: #F9E79F;
    font-weight: bold;
}

/* AI text */
.ai-text {
    color: #D6EAF8;
}

/* Footer note */
.footer-note {
    text-align: center;
    color: #D6EAF8;
    font-size: 14px;
    margin-top: 40px;
    opacity: 0.8;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## 🧾 Chat History")
    if st.session_state.conversation:
        for i, (q, _) in enumerate(st.session_state.conversation[::-1], 1):
            st.markdown(f"**{i}.** {q[:40]}...")
    else:
        st.info("No conversations yet")

# ---------------- MAIN UI ----------------
st.markdown('<div class="main-title">🤖 AI Study Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Ask your questions and get instant help</div>', unsafe_allow_html=True)

# ---------------- INPUT FORM (ENTER ENABLED) ----------------
with st.form(key="question_form", clear_on_submit=True):
    st.markdown('<div class="ask-label">Ask a Question</div>', unsafe_allow_html=True)
    question = st.text_input("", placeholder="Type your question and press Enter...")
    submitted = st.form_submit_button("Ask AI")

    if submitted and question.strip():
        response = f"I received your question: **{question}**. AI response will appear here."
        st.session_state.conversation.append((question, response))

# ---------------- CONVERSATION DISPLAY ----------------
if st.session_state.conversation:
    st.markdown("### 💬 Conversation")
    for q, a in st.session_state.conversation[::-1]:
        st.markdown(f"""
        <div class="chat-box">
            <div class="user-text">You:</div>
            <div>{q}</div>
            <br>
            <div class="ai-text"><b>AI:</b> {a}</div>
        </div>
        """, unsafe_allow_html=True)

# ---------------- FOOTER NOTE ----------------
st.markdown("""
<div class="footer-note">
⚠️ I can make mistakes. Please verify important information.
</div>
""", unsafe_allow_html=True)
