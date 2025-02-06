# CSS styles for the application
MAIN_CSS = """
/* Hide sidebar */
section[data-testid="stSidebar"] {
    display: none;
}

/* Make the title more compact on mobile */
.stTitle {
    font-size: 1.5rem !important;
    padding-top: 0.5rem !important;
}

/* Adjust button styling for mobile */
.stButton button {
    width: 100%;
    border-radius: 20px;
    padding: 0.5rem 1rem;
}

/* Improve spacing on mobile */
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

/* Make expander more touch-friendly */
.streamlit-expanderHeader {
    font-size: 1.2rem;
    padding: 0.75rem !important;
}
"""

def apply_styles():
    """
    Apply the CSS styles to the Streamlit app
    """
    import streamlit as st
    st.markdown(f'<style>{MAIN_CSS}</style>', unsafe_allow_html=True)

def get_mobile_styles():
    return """
    <style>
        /* Center all content */
        .main > div {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }
        
        /* Hide sidebar and fullscreen button */
        [data-testid="collapsedControl"] {
            display: none
        }
        .css-1q1n0ol {
            display: none;
        }
        
        /* Mobile-friendly container */
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
            max-width: 95vw;
        }
        
        /* Enhance title for mobile */
        h1 {
            font-size: 2rem !important;
            margin-bottom: 0.5rem !important;
            text-align: center;
        }
        
        /* Style description text */
        .description {
            font-size: 1rem;
            line-height: 1.5;
            margin-bottom: 1.5rem;
            text-align: center;
        }
        
        /* Style the file uploader */
        .stFileUploader {
            display: flex;
            justify-content: center;
            margin: 2rem 0;
        }
        
        .stFileUploader > div {
            width: 85%;
            max-width: 320px;
        }
        
        .stFileUploader > div > div {
            background: linear-gradient(135deg, #00C6FF 0%, #0072FF 100%);
            color: white;
            padding: 1.5rem 2.5rem;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1.3rem;
            font-weight: 500;
            text-align: center;
            box-shadow: 0 10px 20px rgba(0, 114, 255, 0.2);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }
        
        .stFileUploader > div > div:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 30px rgba(0, 114, 255, 0.3);
            background: linear-gradient(135deg, #00B4FF 0%, #0063FF 100%);
        }
        
        .stFileUploader > div > div:active {
            transform: translateY(1px);
            box-shadow: 0 5px 15px rgba(0, 114, 255, 0.2);
        }
        
        /* Hide the default "Drag and drop" text */
        .stFileUploader > div > div > small {
            display: none;
        }
        
        /* Style the "Browse files" text */
        .stFileUploader > div > div > div {
            color: white;
            font-weight: 500;
        }
        
        /* Add camera icon */
        .stFileUploader > div > div::before {
            content: "📸";
            margin-right: 10px;
            font-size: 1.4rem;
        }
        
        /* Style progress elements */
        .stProgress > div > div {
            border-radius: 10px;
            background: linear-gradient(90deg, #00C6FF 0%, #0072FF 100%);
        }
        
        .step-text {
            margin-top: 0.5rem;
            font-size: 0.9rem;
            color: #666;
            text-align: center;
        }
    </style>
    """

def get_card_container():
    return """
        background-color: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    """

def get_error_container():
    return """
        background-color: #FF4B4B22;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    """

def get_info_container():
    return """
        background-color: #0096FF22;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    """ 