import streamlit as st
import pytesseract
from PIL import Image
import google.generativeai as genai

# Configure Google Generative AI
genai.configure(api_key='api-key')

# Function to convert an uploaded image to text
def image_to_text(image):
    try:
        return pytesseract.image_to_string(image)
    except Exception as e:
        st.error(f"Error extracting text from image: {e}")
        return None

# Function to generate content using Google Generative AI
def generate_content(prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        return model.generate_content(prompt)
    except Exception as e:
        st.error(f"Error generating content: {e}")
        return None

# Streamlit app
def main():
    st.title("Report Analysis")

    # Image upload input
    uploaded_image = st.file_uploader("Upload a test report image (PNG, JPG, JPEG):", type=["png", "jpg", "jpeg"])

    # Text input for keywords
    keywords = "What are the precautions and suggested diet and Give the nutrition deficiency it occured from?"

    # Button for generating summary
    if st.button("Generate Summary") and uploaded_image:
        image = Image.open(uploaded_image)
        text = image_to_text(image)

        if text:
            prompt = (
                f"You are an AI health assistant that generates a summary based on a health test report provided as text. "
                f"The extracted report text is:\n{text} \n"
            )
            generated_summary = generate_content(prompt)
            
            if generated_summary:
                st.subheader("Generated Summary:")
                st.markdown(generated_summary.text)

    # Button for generating in-depth notes based on keywords
    if st.button("Generate In-depth Notes") and uploaded_image and keywords:
        image = Image.open(uploaded_image)
        text = image_to_text(image)

        if text:
            prompt = (
                f"You are an AI health assistant providing in-depth notes based on a health report and specific health-related keywords. "
                f"Keywords: {keywords.strip()} \n\nReport Text:\n{text}\n\n"
                "Provide detailed health advice, dietary suggestions, and possible precautions based on the test results."
            )
            generated_notes = generate_content(prompt)
            
            if generated_notes:
                st.subheader("Generated In-depth Notes:")
                st.markdown(generated_notes.text)

if __name__ == "__main__":
    main() 