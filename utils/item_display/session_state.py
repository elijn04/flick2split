import streamlit as st

def initialize_session_state():
    """Initialize session state variables."""
    if 'guests' not in st.session_state:
        st.session_state.guests = []  # List to store all Guest objects
    
    if 'updated_data' not in st.session_state:
        st.session_state.updated_data = None  # Proper initialization ✅
    
    if 'checkbox_states' not in st.session_state:
        st.session_state.checkbox_states = {}  # Dictionary to track checkbox states
    
    if 'form_submitted' not in st.session_state:
        st.session_state.form_submitted = False  # New flag ✅
