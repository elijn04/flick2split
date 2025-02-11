import streamlit as st
import os
from dotenv import load_dotenv

# Try to load from .env file for local development
load_dotenv()

# Try different methods to get the API key
if os.getenv('GEMINI_API_KEY'):
    API_KEY = os.getenv('GEMINI_API_KEY')
elif 'GEMINI_API_KEY' in st.secrets:
    API_KEY = st.secrets['GEMINI_API_KEY']
else:
    try:
        API_KEY = st.secrets['api']['GEMINI_API_KEY']
    except:
        raise ValueError(
            "GEMINI_API_KEY not found. Please set it in your .env file, "
            "Streamlit secrets, or in the Streamlit Cloud dashboard."
        )

