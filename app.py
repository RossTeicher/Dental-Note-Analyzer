import streamlit as st
from openai import OpenAI, OpenAIError
import os
from PIL import Image
import pytesseract
import tempfile
from pdf2image import convert_from_path
import base64
import re
from fpdf import FPDF

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("🦷 AI Dental Note Generator + Analyzer (w/ Longitudinal Risk + Consent Form)")

procedure_codes = st.text_area("Today's Procedure Codes", "D4341, D4910")
perio_chart_file = st.file_uploader("Upload Perio Chart", type=["png", "jpg", "jpeg", "pdf"])
radiograph_file = st.file_uploader("Upload Radiograph", type=["png", "jpg", "jpeg"])
previous_notes = st.file_uploader("Upload Previous Notes", type=["pdf", "txt"], accept_multiple_files=True)
med_hx = st.text_area("Medical History", "Diabetes, smoking")
today_summary = st.text_area("Today's Clinical Summary", "Generalized 5-6mm pockets, BOP.")

def extract_text(file):
    if file:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name
            try:
                if file.type == "application/pdf":
                    images = convert_from_path(tmp_path)
                    return "\n".join([pytesseract.image_to_string(img) for img in images])
                else:
                    img = Image.open(tmp_path)
                    return pytesseract.image_to_string(img)
            except Exception as e:
                return f"OCR Error: {e}"
    return ""

def combine_notes(files):
    return "\n".join([extract_text(f) for f in files]) if files else ""

def extract_image_data(file):
    if file:
        image_bytes = file.read()
        return base64.b64encode(image_bytes).decode('utf-8')
    return None

def extract_patient_sections(text):
    edu_match = re.search(r"(?si)Patient\s+Education\s+Worksheet\s*[:\-]?\s*\n?(?P<content>.*?)(?=(?:Take[-\s]*Home\s+Patient\s+Warning\s+Sheet|$))", text)
    warn_match = re.search(r"(?si)Take[-\s]*Home\s+Patient\s+Warning\s+Sheet\s*[:\-]?\s*\n?(?P<content>.*?)(?=(?:$))", text)
    edu_content = edu_match.group('content').strip() if edu_match else ""
    warn_content = warn_match.group('content').strip() if warn_match else ""
    return edu_content, warn_content

if st.button("Generate Full Report") and perio_chart_file:
    with st.spinner("Processing patient data..."):
        try:
            perio_text = extract_text(perio_chart_file)
            prior_notes = combine_notes(previous_notes)
            radiograph_encoded = extract_image_data(radiograph_file)

            prompt_content = (
                "Generate:
"
                "1. A complete SOAP note
"
                "2. Periodontal diagnosis
"
                "3. Differential diagnoses
"
                "4. 3 treatment plans (including one with no action)
"
                "5. Risk stratification
"
                "6. Urgency & precautions
"
                "7. Patient Education Worksheet
"
                "8. Take-Home Patient Warning Sheet
"
                "9. A longitudinal risk assessment based on current and prior findings
"
                "10. A smart consent form with risks, disclaimers, and patient-friendly language"
            )

            messages = [
                {"role": "system", "content": "You are a dental AI assistant with expertise in diagnosis, risk scoring, and consent documentation."},
                {"role": "user", "content": f"Procedure codes: {procedure_codes}"},
                {"role": "user", "content": f"Periodontal chart: {perio_text}"},
                {"role": "user", "content": f"Medical history: {med_hx}"},
                {"role": "user", "content": f"Today's clinical summary: {today_summary}"},
                {"role": "user", "content": f"Previous notes: {prior_notes}"},
                {"role": "user", "content": prompt_content}
            ]

            if radiograph_encoded:
                messages.append({"role": "user", "content": f"Radiograph (base64): {radiograph_encoded[:200]}..."})

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )
            output = response.choices[0].message.content

            st.subheader("🧠 Full Output")
            st.text_area("Generated Output", output, height=600)

            edu_text, warn_text = extract_patient_sections(output)
            patient_pdf_text = f"Patient Education Worksheet\n\n{edu_text}\n\nTake-Home Patient Warning Sheet\n\n{warn_text}"

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            for line in patient_pdf_text.split("\n"):
                if line.strip():
                    try:
                        pdf.multi_cell(0, 10, line)
                    except UnicodeEncodeError:
                        pdf.multi_cell(0, 10, line.encode('latin-1', 'replace').decode('latin-1'))

            pdf_path = os.path.join(tempfile.gettempdir(), "patient_summary_output.pdf")
            pdf.output(pdf_path)

            with open(pdf_path, "rb") as f:
                st.download_button("📄 Download Patient PDF", f, file_name="patient_summary_output.pdf", mime="application/pdf")

            consent_match = re.search(r"(?si)Consent Form(?:\:|\s*\n)(.*)", output)
            consent_text = consent_match.group(1).strip() if consent_match else ""

            if consent_text:
                consent_pdf = FPDF()
                consent_pdf.add_page()
                consent_pdf.set_font("Arial", size=12)
                for line in consent_text.split("\n"):
                    if line.strip():
                        try:
                            consent_pdf.multi_cell(0, 10, line)
                        except UnicodeEncodeError:
                            consent_pdf.multi_cell(0, 10, line.encode('latin-1', 'replace').decode('latin-1'))

                consent_pdf_path = os.path.join(tempfile.gettempdir(), "smart_consent_form.pdf")
                consent_pdf.output(consent_pdf_path)

                with open(consent_pdf_path, "rb") as cf:
                    st.download_button("📑 Download Smart Consent Form", cf, file_name="smart_consent_form.pdf", mime="application/pdf")

        except OpenAIError as e:
            st.error(f"OpenAI API error: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
