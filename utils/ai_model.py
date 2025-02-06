import google.generativeai as genai
import os
from config import API_KEY
import streamlit as st

# Configure API key (this runs once)
os.environ["API_KEY"] = API_KEY
genai.configure(api_key=os.environ["API_KEY"])

# Cache the model initialization
@st.cache_resource
def load_model():
    return genai.GenerativeModel(model_name="gemini-1.5-flash")

# Cache the AI processing for same images
@st.cache_data
def ai_return(preprocessed_image):
    # Get the cached model
    model = load_model()
    
    prompt = """
    Extract all relevant data from the receipt in the image and return it in the following structured format:
    {
        "Store Name": "",
        "Date": "",
        "Time": "",
        "Items": [
            {"Name": "", "Quantity": "", "Price": ""}
        ],
        "Subtotal": "",
        "Tax": "",
        "Total": ""
    }
    """

    response = model.generate_content([{'mime_type': 'image/jpeg', 'data': preprocessed_image}, prompt])
    return response.text
