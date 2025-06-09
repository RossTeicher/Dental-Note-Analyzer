
import streamlit as st
from openai import OpenAI
import os
from PIL import Image
import pytesseract
import tempfile
from pdf2image import convert_from_path
from openai import OpenAI, OpenAIError

# Set your OpenAI key from Streamlit secrets
oai_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=oai_key)

st.title("🦷 AI Dental Note Generator")

st.markdown("""
Upload the day's dental data:
1. Procedure Codes (e.g., D1110, D4341)
2. Perio Chart (PDF or Image)
3. Radiograph (optional for now)
""")

procedure_codes = st.text_area("Enter procedure codes or summary", "D1110, D4341")

perio_chart_file = st.file_uploader("Upload Perio Chart (Image or PDF)", type=["png", "jpg", "jpeg", "pdf"])
radiograph_file = st.file_uploader("Upload Radiograph (optional)", type=["png", "jpg", "jpeg"])

def extract_text_from_file(uploaded_file):
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name
            try:
                if uploaded_file.type == "application/pdf":
                    images = convert_from_path(tmp_path)
                    text = "\n".join([pytesseract.image_to_string(img) for img in images])
                else:
                    image = Image.open(tmp_path)
                    text = pytesseract.image_to_string(image)
                return text
            except Exception as e:
                st.error(f"OCR Error: {e}")
    return ""

generate_button = st.button("Generate Note")

if generate_button and procedure_codes and perio_chart_file:
    with st.spinner("Analyzing data and generating note..."):
        try:
            # Extract text from perio chart
            perio_text = extract_text_from_file(perio_chart_file)

            # Compose the prompt for GPT
            messages = [
                {"role": "system", "content": "You are a dental assistant helping to generate SOAP notes."},
                {"role": "user", "content": f"Here are the procedure codes: {procedure_codes}"},
                {"role": "user", "content": f"Here is the perio chart data: {perio_text}"},
                {"role": "user", "content": "Based on this information, generate a periodontal diagnosis and a complete clinical note."}
            ]

            # Call GPT
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=messages
            )

            output = response.choices[0].message.content

            st.subheader("Generated Note")
            st.text_area("Output", output, height=400)

        except OpenAIError as e:
            st.error(f"OpenAI API error: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
else:
    st.info("Please enter procedure codes and upload a perio chart.")
