import base64
from PIL import Image
import io

def preprocess_image(image_file):
    """
    Preprocess the uploaded image and return a Base64-encoded string.
    This includes converting the image to grayscale without resizing it.
    """
    # Open the image using PIL
    image = Image.open(image_file)

    # Convert the image to grayscale
    image = image.convert("L")

    # Save the processed image to a BytesIO object
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)

    # Encode the processed image as Base64
    encode_image = base64.b64encode(buffer.read()).decode("utf-8")

    return encode_image
