import streamlit as st
from utils.ai_model import ai_return
from utils.image_preprocessing import preprocess_image
from utils.data_processing import manually_parse_to_dict
from utils.user_confirmation import user_confirmation
import time

# Hide sidebar with CSS
st.set_page_config(initial_sidebar_state="collapsed")
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

# Title and Description
st.title("Welcome to Flick2Split")
st.markdown(
    """
    ### The Best Bill Splitting App for Meals with Friends
    Upload an image of your receipt, and we’ll help you split the bill among your group in seconds!
    """
)

# Image uploader
image_file = st.file_uploader(label="Upload your receipt here", type=["png", "jpg", "jpeg", "heic"])

if image_file:
    # Validate file type
    if image_file.type not in ["image/png", "image/jpeg", "image/jpg", "image/heic"]:
        st.error("Invalid file type. Please upload a PNG, JPG, JPEG, or HEIC file.")
        st.stop()

    try:
        with st.spinner("Processing your receipt..."):
            # Preprocess the image
            preprocessed_image = preprocess_image(image_file)
            
            # Process the image using AI model
            receipt_data = ai_return(preprocessed_image)
            
            # Manually parse the AI output
            processed_receipt_data = manually_parse_to_dict(receipt_data)
            
            # Set the processed_receipt_data in the session state
            #st.session_state.processed_receipt_data = processed_receipt_data

            # Get user confirmation and updates
            updated_data = user_confirmation(processed_receipt_data)
            
            if updated_data != None: 
                if st.button("Continue"):
                    if updated_data != processed_receipt_data:
                        st.success("Changes saved!")
                        time.sleep(1)
                    st.write("Switching Page ...")
                    # Store updated_data in session state
                    if updated_data is not None:
                        st.session_state.updated_data = updated_data

                    st.switch_page("pages/item_display.py")
                    
            

    except Exception as error:
        st.error(f"An error occurred: {error}")
        st.error(f"Details: {str(error)}")
else:
    st.info("Please upload a receipt to get started.")