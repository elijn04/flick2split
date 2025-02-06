import streamlit as st
import pandas as pd
from utils.shared_item import SharedItem, update_shared_receipt_data

# Set page config must be the first Streamlit command
st.set_page_config(
    page_title="Shared Items",
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

st.title("Shared Items")

# Check for receipt data
if "updated_receipt_data" not in st.session_state:
    st.error("No receipt data found. Please upload a receipt first.")
    if st.button("Return to Upload"):
        st.switch_page("app.py")
else:
    # Ask about shared items
    shared_items_response = st.radio(
        "**Did anyone share any items?**",
        options=["Yes", "No"],
        horizontal=True,
        index=None  # This makes it so no option is pre-selected
    )

    if shared_items_response == "Yes":
        st.write("Select all shared items:")
        
        items = st.session_state.updated_receipt_data["items"]
        
        # Initialize shared items storage with share counts
        if "shared_items_with_shares" not in st.session_state:
            st.session_state.shared_items_with_shares = {}
        
        selected_items = {}
        preview_items = []
        
        # Process each item
        for item in items:
            item_key = f"shared_{item['Name']}"
            
            # Checkbox for item selection
            if st.checkbox(
                f"{item['Name']} (${item['Price']:.2f})",
                key=item_key
            ):
                # Show shares selector for this specific item
                col1, col2 = st.columns([2, 3])
                with col1:
                    st.write("Shared how many ways?")
                with col2:
                    # First show standard options 2-5
                    shares_choice = st.radio(
                        "",
                        options=["2", "3", "4", "5", "Custom"],
                        horizontal=True,
                        key=f"choice_{item_key}"
                    )
                    
                    # If Custom is selected, show number input
                    if shares_choice == "Custom":
                        shares = st.number_input(
                            "Enter number of sharers:",
                            min_value=2,
                            max_value=20,
                            value=6,
                            key=f"custom_shares_{item_key}"
                        )
                    else:
                        shares = int(shares_choice)
                    
                selected_items[item['Name']] = {
                    'item': item,
                    'shares': shares
                }
                
                # Preview this specific split item
                split_price = round(item['Price'] / shares, 2)
                st.markdown("---")  # Add a separator between items
        
        if selected_items:
            # Update session state
            st.session_state.shared_items_with_shares = selected_items
            
            # Create updated receipt data
            shared_receipt = st.session_state.updated_receipt_data.copy()
            new_items = []
            
            # Process each item from the original receipt
            for item in shared_receipt['items']:
                if item['Name'] in selected_items:
                    # Get the shares count for this specific item
                    share_info = selected_items[item['Name']]
                    shared_item = SharedItem(item, share_info['shares'])
                    new_items.append(shared_item.to_dict())
                else:
                    new_items.append(item)
            
            shared_receipt['items'] = new_items
            st.session_state.shared_updated_receipt_data = shared_receipt
            
            
            if st.button("Continue"):
                st.switch_page("pages/item_display.py")
    
    elif shared_items_response == "No":
        # If no shared items, just copy the original receipt data
        st.session_state.shared_updated_receipt_data = (
            st.session_state.updated_receipt_data.copy()
        )
        st.session_state.shared_items = []
        if st.button("Continue"):
            st.switch_page("pages/item_display.py") 