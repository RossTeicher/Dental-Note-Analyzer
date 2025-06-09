
import streamlit as st
from openai import OpenAI
import os
from PIL import Image
import pytesseract
import tempfile
from pdf2image import convert_from_path
from openai import OpenAI, OpenAIError
import base64
from fpdf import FPDF

# Set your OpenAI key from Streamlit secrets
oai_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=oai_key)

st.title("🦷 AI Dental Note Generator + In-Depth Analyzer")

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

def extract_radiograph_summary(file):
    if file:
        image_bytes = file.read()
        encoded = base64.b64encode(image_bytes).decode('utf-8')
        return {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{encoded}"
            }
        }
    return None

generate_button = st.button("Generate Note and Diagnosis")

if generate_button and procedure_codes and perio_chart_file:
    with st.spinner("Analyzing data and generating output..."):
        try:
            perio_text = extract_text_from_file(perio_chart_file)
            radiograph_summary = extract_radiograph_summary(radiograph_file)

            messages = [
                {"role": "system", "content": "You are an expert dental AI assistant trained to provide in-depth diagnostic assessments and treatment planning."},
                {"role": "user", "content": f"Procedure codes performed today: {procedure_codes}"},
                {"role": "user", "content": f"Periodontal chart data: {perio_text}"},
                {"role": "user", "content": "Based on the provided clinical information, generate:\n1. A complete SOAP clinical note\n2. A detailed periodontal diagnosis\n3. A list of possible differential diagnoses for any findings\n4. At least three treatment plan options including one that takes no action, with pros and cons of each. The treatment options should cover general, cosmetic, surgical, and prosthetic possibilities — including implants, veneers, crowns, bridges, scaling and root planing,...
            ]

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )

            output = response.choices[0].message.content

            st.subheader("AI-Generated Note, Diagnosis & Plans")
            st.text_area("Output", output, height=500)

            if output:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.set_font("Arial", size=12)
                for line in output.split("\n"):
                    if line.strip():
                        safe_line = line.encode('latin-1', 'replace').decode('latin-1')
                        pdf.multi_cell(0, 10, safe_line)
                pdf_file_path = os.path.join(tempfile.gettempdir(), "patient_output.pdf")
                pdf.output(pdf_file_path)
                with open(pdf_file_path, "rb") as f:
                    st.download_button(label="📄 Download PDF for Patient", data=f, file_name="patient_output.pdf", mime="application/pdf")

        except OpenAIError as e:
            st.error(f"OpenAI API error: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
else:
    st.info("Please enter procedure codes and upload a perio chart.")
