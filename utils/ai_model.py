import google.generativeai as genai
import os
from config import API_KEY

# Step 1: Configure the Google Generative AI API key
os.environ["API_KEY"] = API_KEY
genai.configure(api_key=os.environ["API_KEY"])

def ai_return(preprocessed_image):
    # Step 4: Choose the Gemini Flash model
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    # Step 5: Provide a text prompt tailored for structured data extraction
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

    # Step 6: Make the API request
    response = model.generate_content([{'mime_type': 'image/jpeg', 'data': preprocessed_image}, prompt])

    # Step 7: Print the structured response
    return response.text
