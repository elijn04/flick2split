import streamlit as st
from utils.item_display.session_state import initialize_session_state
from utils.item_display.utils import gather_user_data

# Initialize session state
initialize_session_state()

# Set a mobile-friendly title and layout
st.set_page_config(page_title="Flick to Split", layout="centered")

# Hide the sidebar using CSS
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Flick to Split 🧾")

# Add some spacing for better readability
st.write("---")  # Horizontal line for visual separation

# Debugging: Check if updated_data exists
# st.write("Session State Keys:", list(st.session_state.keys()))  # Debugging output

if 'updated_data' in st.session_state and st.session_state.updated_data:
    updated_data = st.session_state.updated_data
    # st.write("Updated Data:", updated_data)  # Debugging output

    # Gather user data and create a Guest object
    guest = gather_user_data(updated_data)

    # Assuming st.session_state.guests is a list of guest objects
    if st.session_state.guests:
        for guest in st.session_state.guests:
            # Use columns to display the super summary and expander neatly
            col1, col2 = st.columns([0.8, 0.2])
            
            with col1:
                # Display the super summary
                guest.display_super_summary()
            
            with col2:
                # Add a small spacer for better alignment
                st.write("")  # Empty space
                # Create an expander for the detailed summary
                with st.expander("🔍"):
                    guest.display_summary()
        
        # Add a horizontal line for separation
        st.write("---")
        
    
        
        # Add a button to reset or go back
        if st.button("Reset and Return to Home"):
            st.session_state.updated_data = None  # Reset session state
            st.switch_page("app.py")
            st.rerun()

else:
    # Display an error message with better spacing
    st.error("No updated data found. Please return to the home page and upload a receipt.")
    
    # Add a button to return to the home page
    if st.button("Return to Home"):
        st.session_state.updated_data = None  # Reset session state
        st.switch_page("app.py")
        st.rerun()