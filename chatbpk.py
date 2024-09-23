import streamlit as st
import os
from dotenv import load_dotenv, find_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv(find_dotenv(), override=True)

# Configure the Gemini API
genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

# Initialize the Gemini model
model = genai.GenerativeModel(model_name='models/gemini-1.5-pro-latest')

def generate_response(prompt):
    response = model.generate_content(prompt)
    return response.text

# Streamlit app
st.title("Gemini AI Assistant")

# User input
user_prompt = st.text_area("Enter your prompt:", height=100)

if st.button("Generate Response"):
    if user_prompt:
        with st.spinner("Generating response..."):
            response = generate_response(user_prompt)
            st.text_area("Response:", value=response, height=300, disabled=True)
    else:
        st.warning("Please enter a prompt.")

# Add a note about the model being used
st.sidebar.markdown("Using Gemini 1.5 Pro model")