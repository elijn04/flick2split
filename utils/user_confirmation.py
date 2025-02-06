import streamlit as st
import pandas as pd


def edit_dictionary(processed_receipt_data):
    """
    Allows the user to edit the receipt data by selecting a tip percentage and adjusting item details.
    
    The function updates the session state with tip information and, once the tip input is interacted with,
    displays an editable table of items along with subtotal, tip, tax, and total calculations.

    Parameters:
        processed_receipt_data (dict): The initial receipt data containing keys like "Tips", "Tax", and "items".

    Returns:
        dict or None: A dictionary with updated receipt data if the user has interacted with the tip input;
                      otherwise, None.
    """
    st.write("### Add Tip")
    
    if "tips" not in st.session_state:
        st.session_state.tips = int(processed_receipt_data.get("Tips", 0))

    # Simple tip selection with columns for better spacing
    col1, col2 = st.columns([2, 1])
    
    with col1:
        tip_options = [
            "No tip (0%)",
            "15% - Standard",
            "20% - Great service",
            "Custom amount"
        ]
        selected_option = st.radio(
            "Select tip amount",
            options=tip_options,
            horizontal=True,
            label_visibility="collapsed"
        )
    
    # Handle tip selection
    if selected_option == "No tip (0%)":
        st.session_state.tips = 0
    elif selected_option == "15% - Standard":
        st.session_state.tips = 15
    elif selected_option == "20% - Great service":
        st.session_state.tips = 20
    elif selected_option == "Custom amount":
        with col2:
            st.session_state.tips = st.number_input(
                "Enter tip percentage",
                value=st.session_state.tips,
                min_value=0,
                max_value=100,
                step=1,
                help="Enter a number between 0-100"
            )

    # Calculate subtotal first
    subtotal = sum(item.get("Price", 0) for item in processed_receipt_data["items"])

    # Use session state to track if the tip input has been interacted with
    if "prev_tips" not in st.session_state:
        st.session_state.prev_tips = int(processed_receipt_data.get("Tips", 0))

    if st.session_state.prev_tips != st.session_state.tips:
        st.session_state.tips_interacted = True

    st.session_state.prev_tips = st.session_state.tips

    # Only proceed if the tip input has been interacted with
    if st.session_state.get("tips_interacted", False):
        
        tip_dollar = subtotal * st.session_state.tips / 100
        st.write(f"**Tip = ${tip_dollar:.2f}**")
        
        # Display Subtotal, Tax, and Total in columns
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("**Subtotal**")
            new_subtotal = st.number_input(
                "Subtotal",
                value=float(subtotal if subtotal is not None else 0.0),
                key="subtotal",
                label_visibility="collapsed"
            )
        with col2:
            st.write("**Tax**")
            tax_value = processed_receipt_data.get("Tax", 0.0)
            updated_tax = st.number_input(
                "Tax",
                value=float(tax_value if tax_value is not None else 0.0),
                key="tax",
                label_visibility="collapsed"
            )
        with col3:
            st.write("**Total** (tip & tax included)")
            total = new_subtotal + updated_tax + tip_dollar
            new_total = st.number_input(
                "Total",
                value=float(total if total is not None else 0.0),
                key="total",
                label_visibility="collapsed",
                disabled=True
            )
        st.write("If the subtotal is correct, the items are likely accurate. ")
        
        # Add button to show/hide items
        if "show_items" not in st.session_state:
            st.session_state.show_items = False
            
        if st.button("Double Check Items" if not st.session_state.show_items else "Hide Items"):
            st.session_state.show_items = not st.session_state.show_items
        
        # Only show items editor when show_items is True
        if st.session_state.show_items:
            st.write("**Click on the item to edit then press continue when done**")
            items_df = pd.DataFrame(processed_receipt_data["items"])
            edited_items_df = st.data_editor(items_df, num_rows="dynamic", use_container_width=True)
            
            # Check if data is missing
            if edited_items_df.isnull().values.any():
                st.warning("Some item details are missing. Please fill in all the details.")
                if len(edited_items_df) > len(items_df):
                    st.error("A new item row has been added. Please fill in all details. If this was accidental, enter 'None' for the name and '0' for both quantity and price.")

            updated_items = edited_items_df.to_dict("records")
        else:
            updated_items = processed_receipt_data["items"]

        if processed_receipt_data["items"] != updated_items:
            st.write("**Subtotal & Total were updated based on the changes you made**")

        # Check if subtotal or total is 0
        if new_subtotal == 0 or new_total == 0:
            st.error("Subtotal or Total cannot be 0. Please check your inputs.")
            st.rerun()  # Refresh the page to prompt the user to re-enter values

        # Create a new dictionary with updated values
        updated_data = {
            "Subtotal": new_subtotal,
            "Tax": updated_tax,
            "Tips": st.session_state.tips,
            "Total": new_total,
            "items": updated_items
        }

        return updated_data
    else:
        return None


def user_confirmation(processed_receipt_data):
    """
    Checks for valid receipt data and allows the user to confirm and edit it.

    Parameters:
        processed_receipt_data (dict): The initial receipt data.

    Returns:
        dict or None: The updated receipt data if editing occurred; otherwise, None.
    """
    if not processed_receipt_data:
        st.error("No receipt data found. Please upload a receipt.")
        return None

    updated_data = edit_dictionary(processed_receipt_data)
    return updated_data
