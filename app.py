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

/* Input box */
.stTextInput input {
    background-color: #1B4F72;
    color: #FDFEFE;
    border-radius: 10px;
    border: 2px solid #74B9FF;
    padding: 10px;
    font-size: 16px;
}

/* Placeholder color */
.stTextInput input::placeholder {
    color: #D6EAF8;
}

/* Button */
.stButton button {
    background-color: #74B9FF;
    color: black;
    font-size: 16px;
    font-weight: bold;
    border-radius: 10px;
    padding: 10px 20px;
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
    margin-left: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- UI ----------------
st.markdown('<div class="main-title">🤖 AI Study Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Ask your questions and get instant help</div>', unsafe_allow_html=True)

# Input
question = st.text_input("Ask a question", placeholder="Type your question here...")

# Session state
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Button
if st.button("Ask AI"):
    if question.strip() != "":
        # Temporary AI response (no API)
        response = f"I received your question: **{question}**. AI response will appear here."

        st.session_state.conversation.append(
            (question, response)
        )

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
