import streamlit as st
from utils.item_display.utils import gather_user_data
from utils.item_display.session_state import initialize_session_state

# Set page config must be the first Streamlit command
st.set_page_config(
    page_title="Select Items",
    initial_sidebar_state="collapsed"
)

# Hide sidebar with CSS
st.markdown(
    """
    <style>
        [data-testid="collapsedControl"] {
            display: none
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Select Your Items")

# Check if we have receipt data
if "shared_updated_receipt_data" not in st.session_state:
    st.error("No receipt data found. Please upload a receipt first.")
    if st.button("↩️ Return Home"):
        st.switch_page("app.py")
else:
    # Get the updated receipt data
    receipt_data = st.session_state.shared_updated_receipt_data

    # Gather user data and create a Guest object
    guest = gather_user_data(receipt_data)

    # Display summary of all guests' selections
    if st.session_state.guests:
        st.write("### Current Selections")
        for guest in reversed(st.session_state.guests):
            # Use columns to display the super summary and expanders neatly
            col1, col2 = st.columns([0.8, 0.2])
            
            with col1:
                # Display the super summary
                guest.display_super_summary()
            
            with col2:
                # Create an expander for the detailed summary
                with st.expander("🔍"):
                    guest.display_summary()

    # Add navigation buttons at the bottom
    if st.button("← Back"):
        # Clear relevant session state data
        st.session_state.shared_updated_receipt_data = None
        st.session_state.guests = []  # Clear guests list
        st.session_state.item_display_back_pressed = True
        st.switch_page("pages/2_Shared_Items.py") 