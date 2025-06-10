import streamlit as st
from openai import OpenAI, OpenAIError
import os
import pandas as pd
import matplotlib.pyplot as plt
import tempfile
import csv
from datetime import datetime
from fpdf import FPDF
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from synthesia_stub import generate_synthesia_script
from procedure_list import procedures
from lang_map import lang_map

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("🦷 Dental AI Suite with Synthesia Integration")

# Input fields
st.header("📋 Patient Data Entry")
procedure_codes = st.text_area("Procedure Codes", "D1110, D4341")
notes = st.text_area("Clinical Notes", "Patient presents with gingival inflammation and localized bone loss.")
perio_chart = st.file_uploader("Upload Perio Chart (PDF/Image)", type=["pdf", "png", "jpg", "jpeg"])
radiograph_file = st.file_uploader("Upload Radiograph (optional)", type=["png", "jpg", "jpeg"])
patient_name = st.text_input("Patient Full Name")
category = st.selectbox("Procedure Category", list(procedures.keys()))
procedure = st.selectbox("Procedure", procedures[category])
language = st.selectbox("Language for Consent & Video", list(lang_map.keys()))
case_accepted = st.radio("Case Accepted?", ["Yes", "No"])
signature = st.text_input("Type Signature")

def extract_text(file):
    if file:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name
        if file.type == "application/pdf":
            images = convert_from_path(tmp_path)
            return "\n".join([pytesseract.image_to_string(img) for img in images])
        else:
            image = Image.open(tmp_path)
            return pytesseract.image_to_string(image)
    return ""

if st.button("Generate Full Report"):
    with st.spinner("Generating..."):
        try:
            perio_text = extract_text(perio_chart)
            diagnostic_prompt = f"""You are an expert dental assistant AI. Based on the input below, generate:
1. Complete SOAP note
2. Periodontal diagnosis
3. Differential diagnoses
4. Treatment options (including no action)
5. Risk stratification
6. Personalized urgency and precautions
7. Plain-language patient summary
8. Take-home warning sheet

Procedure codes: {procedure_codes}
Clinical notes: {notes}
Perio chart: {perio_text}
"""
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": diagnostic_prompt}]
            )
            result = response.choices[0].message.content
            st.subheader("📝 Full Diagnostic Report")
            st.text_area("Clinical Output", result, height=400)

            # Consent form
            consent_prompt = f"""Write a consent form for {procedure} in {language}. Use simple language and include:
- Procedure explanation
- Risks, benefits, alternatives
- Legal disclaimer
- Post-op instructions
"""
            consent_response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": consent_prompt}]
            )
            consent = consent_response.choices[0].message.content
            st.subheader("📄 Consent Form")
            st.text_area("Consent Text", consent, height=300)

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            for line in consent.split("\n"):
                try:
                    pdf.multi_cell(0, 10, line)
                except:
                    pdf.multi_cell(0, 10, line.encode("latin-1", "replace").decode("latin-1"))
            pdf.ln(10)
            pdf.cell(0, 10, f"Signature: {signature}", ln=True)

            file_path = os.path.join(tempfile.gettempdir(), f"{patient_name}_report.pdf")
            pdf.output(file_path)
            with open(file_path, "rb") as f:
                st.download_button("📥 Download Consent PDF", f, file_name=f"{patient_name}_report.pdf")

            with open("case_acceptance_log.csv", "a", newline="") as logf:
                writer = csv.writer(logf)
                writer.writerow([datetime.now().isoformat(), patient_name, procedure, language, case_accepted])
        except Exception as e:
            st.error(f"Error: {e}")

# Analytics Dashboard
st.sidebar.header("📊 Case Acceptance Analytics")
if os.path.exists("case_acceptance_log.csv"):
    df = pd.read_csv("case_acceptance_log.csv", header=None, names=["Timestamp", "Patient", "Procedure", "Language", "Accepted"])
    fig, ax = plt.subplots()
    df["Accepted"].value_counts().plot(kind="bar", ax=ax, title="Case Acceptance")
    st.sidebar.pyplot(fig)

# Synthesia Script and Playback
st.header("🎥 Synthesia Patient Video")
if st.button("Generate Synthesia Script"):
    script = generate_synthesia_script(procedure, language)
    st.text_area("Synthesia Video Script", script, height=250)
    st.markdown("### ▶️ Example Video (Placeholder)")
    st.video("https://cdn.synthesia.io/examples/website-demo.mp4")
