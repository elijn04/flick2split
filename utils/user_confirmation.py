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
    st.write("### Select Tip Percentage")

    # Initialize session state for tips if it doesn't exist
    if "tips" not in st.session_state:
        st.session_state.tips = int(processed_receipt_data.get("Tips", 0))

    # Tip selection buttons
    tip_col1, tip_col2, tip_col3 = st.columns(3)
    with tip_col1:
        if st.button("15% Tip"):
            st.session_state.tips = 15
    with tip_col2:
        if st.button("20% Tip"):
            st.session_state.tips = 20
    with tip_col3:
        custom_tip = st.number_input(
            "Custom Tip (%)",
            value=st.session_state.get("tips", 0),
            min_value=0,
            key="custom_tip",
            step=1
        )
        if custom_tip:
            st.session_state.tips = custom_tip

    # Use session state to track if the tip input has been interacted with
    if "prev_tips" not in st.session_state:
        st.session_state.prev_tips = int(processed_receipt_data.get("Tips", 0))

    if st.session_state.prev_tips != st.session_state.tips:
        st.session_state.tips_interacted = True

    st.session_state.prev_tips = st.session_state.tips

    # Only proceed if the tip input has been interacted with
    if st.session_state.get("tips_interacted", False):
        st.subheader("Doesn't Hurt to double check!")
        st.write("Our Ai is 95% accurate, you can edit the values below if needed.")

        # Items editing section
        st.write("### Items")
        items_df = pd.DataFrame(processed_receipt_data["items"])
        edited_items_df = st.data_editor(items_df, num_rows="dynamic", use_container_width=True)
        # Check if data is missing
        if edited_items_df.isnull().values.any():
            st.warning("Some item details are missing. Please fill in all the details.")
            # Check if a new row was added
            if len(edited_items_df) > len(items_df):
                st.error("A new item row has been added. Please fill in all details. If this was accidental, enter 'None' for the name and '0' for both quantity and price.")

        updated_items = edited_items_df.to_dict("records")

        

        # Calculate subtotal based on the updated items
        subtotal = sum(item.get("Price", 0) for item in updated_items)

        if processed_receipt_data["items"] != updated_items:
            st.write("**Subtotal & Total were updated based on the changes you made**")

        # Display Subtotal, Tip (in $), Tax, and Total in columns
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.write("**Subtotal**")
            new_subtotal = st.number_input(
                "Subtotal",
                value=float(subtotal if subtotal is not None else 0.0),
                key="subtotal",
                label_visibility="collapsed"
            )
        with col2:
            st.write("**Tip ($)**")
            tip_dollar = new_subtotal * st.session_state.tips / 100
            st.number_input(
                "Tip", 
                value=float(tip_dollar), 
                key="tip_dollar", 
                label_visibility="collapsed",
                disabled=True
            )
        with col3:
            st.write("**Tax**")
            tax_value = processed_receipt_data.get("Tax", 0.0)
            updated_tax = st.number_input(
                "Tax",
                value=float(tax_value if tax_value is not None else 0.0),
                key="tax",
                label_visibility="collapsed"
            )
        with col4:
            st.write("**Total** (tip & tax included)")
            total = new_subtotal + updated_tax + tip_dollar
            new_total = st.number_input(
                "Total",
                value=float(total if total is not None else 0.0),
                key="total",
                label_visibility="collapsed",
                disabled=True
            )

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
