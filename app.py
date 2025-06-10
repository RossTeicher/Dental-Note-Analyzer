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

st.title("🦷 Phase 7: Longitudinal Risk + Smart Consent Generator")

procedure_codes = st.text_area("Today's Procedure Codes", "D4341, D4910")
perio_chart_file = st.file_uploader("Upload Perio Chart", type=["png", "jpg", "jpeg", "pdf"])
previous_notes = st.file_uploader("Upload Previous Notes", type=["pdf", "txt"], accept_multiple_files=True)
med_hx = st.text_area("Medical History (optional)", "Diabetes, smoking")
today_summary = st.text_area("Today's Clinical Summary", "Generalized 5-6mm pockets, BOP, calculus subgingivally.")

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

if st.button("Generate Risk Assessment + Consent Form") and perio_chart_file:
    with st.spinner("Processing..."):
        try:
            perio_text = extract_text(perio_chart_file)
            prior_notes = combine_notes(previous_notes)

            messages = [
                {"role": "system", "content": "You are a dental AI trained to assess risk over time and generate consent forms."},
                {"role": "user", "content": f"Today's procedures: {procedure_codes}"},
                {"role": "user", "content": f"Perio chart: {perio_text}"},
                {"role": "user", "content": f"Medical history: {med_hx}"},
                {"role": "user", "content": f"Today's summary: {today_summary}"},
                {"role": "user", "content": f"Previous notes: {prior_notes}"},
                {"role": "user", "content": "Perform a longitudinal risk assessment based on current and prior findings, systemic risks, and prior recommendations. Then, generate a smart, patient-friendly consent form for today’s planned procedures including legal disclaimers and risks of not proceeding with treatment."}
            ]

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )

            output = response.choices[0].message.content
            st.subheader("🧠 AI Output")
            st.text_area("Generated Content", output, height=600)

            consent_match = re.search(r"(?si)Consent Form(?:\:|\s*
)(.*)", output)
            consent_text = consent_match.group(1).strip() if consent_match else "Consent form content not found."

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            for line in consent_text.split("\n"):
                if line.strip():
                    try:
                        pdf.multi_cell(0, 10, line)
                    except UnicodeEncodeError:
                        pdf.multi_cell(0, 10, line.encode('latin-1', 'replace').decode('latin-1'))

            pdf_path = os.path.join(tempfile.gettempdir(), "longitudinal_consent_form.pdf")
            pdf.output(pdf_path)

            with open(pdf_path, "rb") as f:
                st.download_button("📄 Download Consent Form PDF", f, file_name="longitudinal_consent_form.pdf", mime="application/pdf")

        except OpenAIError as e:
            st.error(f"OpenAI API error: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
