from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load the Gemini AI model
model = genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(input_text, image_data, prompt):
    """Generate a response from the Gemini AI model."""
    response = model.generate_content([input_text, image_data[0], prompt])
    return response.text

def input_image_details(uploaded_file):
    """Extract image details from the uploaded file."""
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="MultiLanguage Invoice Extractor")
st.header("MultiLanguage Invoice Extractor")

# User inputs
input_prompt = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image of an invoice...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Give Details about Invoice")

# Prompt for the AI model
input_prompt_text = """
Please upload the invoice document (PDF, image, or other supported formats) to begin the extraction process.
What language is this invoice in? 
You are an expert in understanding invoices.
You will receive input images as invoices &
you will have to answer questions based on the input image.
"""

if submit:
    if input_prompt:  # Check if the input prompt is provided
        try:
            image_data = input_image_details(uploaded_file)
            with st.spinner('Processing...'):
                response = get_gemini_response(input_prompt_text, image_data, input_prompt)
            st.subheader("The Response is:")
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please provide an input prompt.")