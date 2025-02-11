import streamlit as st

# Set page config must be the first Streamlit command
st.set_page_config(
    page_title="Review Receipt",
    initial_sidebar_state="collapsed"
)

import pandas as pd

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

def handle_tip_selection(subtotal):
    """Handle tip selection and calculation."""
    st.write("### Add Tip")
    
    if "tips" not in st.session_state:
        st.session_state.tips = 0

    col1, col2 = st.columns([2, 1])
    # ... rest of tip selection code ...

def display_receipt_summary(items, tax, tip):
    """Display receipt summary with editable fields."""
    # ... receipt summary code ...

def main():
    st.title("Review Receipt")
    
    # Get receipt data from previous page
    if "receipt_data" not in st.session_state:
        st.error("No receipt data found. Please upload a receipt first.")
        if st.button("↩️ Return Home"):
            st.switch_page("app.py")
        return
    
    receipt_data = st.session_state.receipt_data
    
    # Step 1: Display and edit items
    st.write("### Review Items")
    items_df = pd.DataFrame(receipt_data["items"])
    edited_items = st.data_editor(
        items_df,
        num_rows="dynamic",
        use_container_width=True
    )
    
    # Step 2: Handle tip selection
    tip = handle_tip_selection(receipt_data["Subtotal"])
    
    # Step 3: Display receipt summary
    subtotal, tax, total = display_receipt_summary(
        edited_items.to_dict("records"),
        receipt_data["Tax"],
        tip
    )
    
    # Step 4: Continue button
    if st.button("Continue to Split"):
        updated_data = {
            "Subtotal": subtotal,
            "Tax": tax,
            "Tips": st.session_state.tips,
            "Total": total,
            "items": edited_items.to_dict("records")
        }
        st.session_state.updated_data = updated_data
        st.switch_page("pages/2_shared_items.py")

if __name__ == "__main__":
    main() 