# app.py
import streamlit as st
import os
import openai

st.set_page_config(page_title="AI Study Assistant", page_icon="🤖")

st.title("🤖 AI Study Assistant")
st.write("Ask questions and get answers powered by OpenAI GPT models!")

# --- Step 1: Load API Key ---
openai.api_key = os.getenv("OPENAI_API_KEY")

# Optional fallback if API key not found
if openai.api_key is None:
    st.warning("OpenAI API key not found in secrets. Please enter it below:")
    openai.api_key = st.text_input("Enter your OpenAI API Key", type="password")

# --- Step 2: Get user input ---
user_prompt = st.text_area("Enter your question or prompt here:", height=150)

# --- Step 3: Submit button ---
if st.button("Get Answer"):

    if not user_prompt:
        st.error("Please enter a prompt first!")
    else:
        with st.spinner("Generating response..."):
            try:
                response = openai.Completion.create(
                    model="text-davinci-003",  # or "gpt-3.5-turbo" for chat-like responses
                    prompt=user_prompt,
                    max_tokens=200,
                    temperature=0.7
                )
                answer = response.choices[0].text.strip()
                st.success("✅ Response:")
                st.write(answer)
            except Exception as e:
                st.error(f"Error connecting to OpenAI: {e}")

# --- Step 4: Footer ---
st.markdown("---")
st.markdown(
    "💡 **Tip:** Your OpenAI API key is kept secure using Streamlit Secrets. "
    "If not provided, you can enter it manually above."
)
