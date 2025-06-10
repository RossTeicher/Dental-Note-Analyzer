import streamlit as st
from openai import OpenAI, OpenAIError
import os
import tempfile
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from fpdf import FPDF
import re

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("🦷 AI Dental Suite – Enhanced Note Generator with Scary Sheet & Med History")

# Inputs
procedure_codes = st.text_area("Procedure Codes", "D1110, D4341")
notes = st.text_area("Clinical Notes", "Localized inflammation, probing 6-7mm in posterior.")
medical_history = st.text_area("Relevant Medical History", "Hypertension, diabetic, no known allergies.")
perio_chart = st.file_uploader("Upload Perio Chart (PDF/Image)", type=["pdf", "png", "jpg", "jpeg"])
radiograph = st.file_uploader("Upload Radiograph (optional)", type=["png", "jpg", "jpeg"])

def extract_text(file):
    if file:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(file.read())
            path = tmp.name
        if file.type == "application/pdf":
            return "\n".join([pytesseract.image_to_string(p) for p in convert_from_path(path)])
        else:
            return pytesseract.image_to_string(Image.open(path))
    return ""

def extract_patient_summary(text):
    edu_match = re.search(r"(?si)Patient\s+Education\s+Worksheet.*?:?\s*(.*?)(?=Take[-\s]*Home|$)", text)
    warn_match = re.search(r"(?si)Take[-\s]*Home\s+Patient\s+Warning\s+Sheet.*?:?\s*(.*)", text)
    return (edu_match.group(1).strip() if edu_match else ""), (warn_match.group(1).strip() if warn_match else "")

if st.button("🧠 Generate Note & Patient Handout"):
    with st.spinner("Analyzing patient data..."):
        try:
            perio_text = extract_text(perio_chart)
            full_prompt = (
                f"Procedure codes: {procedure_codes}\n"
                f"Clinical Notes: {notes}\n"
                f"Medical History: {medical_history}\n"
                f"Perio Chart: {perio_text}\n"
                "Generate the following:\n"
                "1. Complete SOAP note\n"
                "2. Perio diagnosis\n"
                "3. Differential diagnoses\n"
                "4. Three treatment options (one with no action)\n"
                "5. Risk stratification\n"
                "6. Treatment urgency\n"
                "7. Patient Education Worksheet\n"
                "8. Take-Home Patient Warning Sheet with strong, scary language to motivate treatment"
            )

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": full_prompt}]
            )

            result = response.choices[0].message.content
            st.subheader("📝 Full Note & Report")
            st.text_area("Generated Report", result, height=400)

            edu, warn = extract_patient_summary(result)
            if edu or warn:
                st.subheader("📄 Take-Home Summary Preview")
                st.markdown("#### Patient Education Worksheet")
                st.info(edu)
                st.markdown("#### Take-Home Warning Sheet")
                st.warning(warn)

                # PDF generation
                pdf = FPDF()
                pdf.add_page()
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.set_font("Arial", size=12)
                for line in (f"Patient Education Worksheet\n\n{edu}\n\nTake-Home Patient Warning Sheet\n\n{warn}").split("\n"):
                    try:
                        pdf.multi_cell(0, 10, line)
                    except UnicodeEncodeError:
                        pdf.multi_cell(0, 10, line.encode("latin-1", "replace").decode("latin-1"))
                pdf_path = os.path.join(tempfile.gettempdir(), "scary_sheet.pdf")
                pdf.output(pdf_path)
                with open(pdf_path, "rb") as f:
                    st.download_button("📥 Download Patient Scary Sheet", f, file_name="take_home_sheet.pdf")

        except OpenAIError as e:
            st.error(f"OpenAI API error: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
