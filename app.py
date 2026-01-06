import google.generativeai as genai
import streamlit as st

# Add your key here directly just for this test
genai.configure(api_key="YOUR_API_KEY_HERE")

st.write("List of available models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        st.write(m.name)
