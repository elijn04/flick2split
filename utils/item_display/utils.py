import streamlit as st
from utils.item_display.guest import Guest
from utils.item_display.session_state import initialize_session_state

def get_guest_name():
    """
    Prompt the user to enter their name.

    Returns:
        str: The name of the guest, or None if no name is entered.
    """
    guest_name = st.text_input("Enter your name:", key="name", placeholder="Enter name here")
    
    # Strip any leading/trailing whitespace and format the name
    if guest_name:
        guest_name = guest_name.strip().title()
        return guest_name
    return None

def display_items_for_selection(guest_name, items):
    """
    Display items with checkboxes for the guest to select.

    Args:
        guest_name (str): The name of the guest.
        items (list): A list of items with their details (name, quantity, price).

    Returns:
        list: A list of selected items, each represented as a dictionary with 'name', 'price', and 'quantity'.
    """
    selected_items = []
    for item in items:
        name = item["Name"]
        quantity = item["Quantity"]
        price = item["Price"]

        # Skip items with invalid price or quantity
        if price <= 0 or quantity <= 0:
            continue

        # Calculate the price per unit
        price_per_unit = price / quantity

        # Display the item multiple times based on its quantity
        for i in range(int(quantity)):
            item_key = f"{guest_name}_{name}_{i}"  # Unique key for each checkbox

            # Initialize checkbox state if not already set
            if item_key not in st.session_state.checkbox_states:
                st.session_state.checkbox_states[item_key] = False

            # Only show the checkbox if it hasn't been submitted
            if not st.session_state.checkbox_states[item_key]:
                if st.checkbox(f"{name} - ${price_per_unit:.2f}", key=item_key):
                    selected_items.append({"name": name, "price": price_per_unit, "quantity": 1})
    return selected_items

def handle_submission(guest, selected_items, updated_data):
    """
    Handle the submission of selected items by updating the session state and removing selected items.

    Args:
        guest (Guest): The Guest object representing the current guest.
        selected_items (list): A list of selected items.
        updated_data (dict): The updated receipt data.
    """
    # Add the guest to the session state
    st.session_state.guests.append(guest)

    # Mark the selected checkboxes as submitted
    for item in selected_items:
        for i in range(item["quantity"]):
            item_key = f"{guest.name}_{item['name']}_{i}"
            st.session_state.checkbox_states[item_key] = True  # Mark as submitted

    # Remove selected items from the updated_data list and update the price
    for item in selected_items:
        for original_item in updated_data["items"]:
            if original_item["Name"] == item["name"]:
                original_item["Price"] -= item["price"]
                original_item["Quantity"] -= 1
                if original_item["Quantity"] == 0:
                    updated_data["items"].remove(original_item)
                break

    if selected_items:
        st.rerun()  # Refresh the page for the next guest

def gather_user_data(updated_data):
    """
    Gather user data and handle checkbox submissions.

    Args:
        updated_data (dict): A dictionary containing the updated receipt data, including items and their quantities.

    Returns:
        Guest: A Guest object representing the current guest and their selected items.
    """
    # Initialize session state variables
    initialize_session_state()

    # Check if there are any items left to select
    if not updated_data.get("items", []):
        return None  # Return early if no items are left

    # Step 1: Ask the user to enter their name
    guest_name = get_guest_name()

    if guest_name:
        # Check if the guest name is already in the list of guests
        st.success(f"Hello, {guest_name}!, Now goodbye please enter name of next guest")
        # Create a Guest object
        guest = Guest(guest_name)
        st.write(f"Hello, {guest.name}! Please select the items you ordered:")

        # Step 2: Display items with checkboxes
        selected_items = display_items_for_selection(guest_name, updated_data["items"])

        # Step 3: Add selected items to the guest's list
        for item in selected_items:
            guest.add_item(item["name"], item["price"])

        # Step 4: Calculate proportional tax and tip
        overall_subtotal = updated_data["Subtotal"]
        overall_tax = updated_data["Tax"]
        overall_tip = updated_data["Tips"]
        guest.calculate_tax_and_tip(overall_subtotal, overall_tax, overall_tip)

        # Step 5: Add a "Submit" button (only visible if items are selected and not already submitted)
        if len(selected_items) > 0 and not st.session_state.form_submitted:
            submit_button = st.button("**Next Guest →**")
            if submit_button:
                handle_submission(guest, selected_items, updated_data)
                st.session_state.form_submitted = True  # Set the flag to True after submission
                st.session_state.name = ""  # Clear the name input
                st.rerun()  # Refresh the page to hide the form

        return guest
    return None