# app.py
import streamlit as st
import os
from openai import OpenAI

st.set_page_config(page_title="AI Study Assistant", page_icon="🤖")

st.title("🤖 AI Study Assistant")
st.write("Ask questions and get answers powered by OpenAI GPT models!")

# --- Step 1: Load API Key ---
api_key = os.getenv("OPENAI_API_KEY")

# Optional fallback if API key not found
if not api_key:
    st.warning("OpenAI API key not found in secrets. Please enter it below:")
    api_key = st.text_input("Enter your OpenAI API Key", type="password")

# Initialize OpenAI client
if api_key:
    client = OpenAI(api_key=api_key)

# --- Step 2: Get user input ---
user_prompt = st.text_area("Enter your question or prompt here:", height=150)

# --- Step 3: Submit button ---
if st.button("Get Answer"):
    if not user_prompt:
        st.error("Please enter a prompt first!")
    else:
        if not api_key:
            st.error("API key required to connect to OpenAI.")
        else:
            with st.spinner("Generating response..."):
                try:
                    # --- NEW OpenAI 1.0+ API call ---
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
