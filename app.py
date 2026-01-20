import streamlit as st
import os
import openai
# Get OpenAI API key from Streamlit Secrets
openai.api_key = os.getenv("OPENAI_API_KEY")
# Optional fallback if secrets not found
if openai.api_key is None:
    openai.api_key = st.text_input("Enter your OpenAI API Key", type="password")
if st.button("Test OpenAI Connection"):
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt="Hello, world!",
            max_tokens=5
        )
        st.write("OpenAI connection successful:", response.choices[0].text)
    except Exception as e:
        st.error(f"Error connecting to OpenAI: {e}")
