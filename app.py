import streamlit as st
from utils.ai_model import ai_return
from utils.image_preprocessing import preprocess_image
from utils.data_processing import manually_parse_to_dict
import time

# Set page config must be the first Streamlit command
st.set_page_config(
    page_title="Flick2Split"
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

# Title and Description
st.title("Flick2Split!")

st.markdown("""
    ### Split Bills with Friends Effortlessly!
    Just snap a photo of your receipt and we'll do the rest.
""")

# Center the upload area using columns
if 'image_file' not in st.session_state:
    st.session_state.image_file = None

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.session_state.image_file is None:
        image_file = st.file_uploader(
            "📸 Upload Receipt",
            type=["png", "jpg", "jpeg", "heic"],
            help="Supported formats: PNG, JPG, JPEG, HEIC"
        )
        if image_file is not None:
            st.session_state.image_file = image_file

if st.session_state.image_file is not None:
    image_file = st.session_state.image_file
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
            
            # Store the initial receipt data
            st.session_state.receipt_data = processed_receipt_data
            
            if st.button("Confirm Receipt"):
                st.switch_page("pages/receipt_confirmation.py")
            
    except Exception as error:
        st.error(f"An error occurred: {error}")
        st.error(f"Details: {str(error)}")
else:
    st.info("Please upload a receipt to get started.")