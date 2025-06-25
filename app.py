
import streamlit as st
from openai import OpenAI
from PIL import Image
import fitz  # PyMuPDF
import os

st.set_page_config(page_title="BrightBite - Dental Note Analyzer", layout="wide")
st.title("🧠🦷 BrightBite - Dental Note Analyzer")

# Secure OpenAI key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Tabs
tabs = st.tabs(["SOAP Note Generator", "Radiograph Analyzer", "PDF & Chart Uploader", 
                "Consent Generator", "Compliance Auditor"])

with tabs[0]:
    st.header("📋 SOAP Note Generator")
    st.write("Automatically generates SOAP notes based on uploaded data.")
    patient_name = st.text_input("Patient Name")
    history = st.text_area("Medical History")
    medications = st.text_area("Current Medications")
    allergies = st.text_area("Allergies")
    findings = st.text_area("Clinical Findings")
    if st.button("Generate SOAP Note"):
        soap_note = f"""
        S: Patient reports {history}
        O: Medications include {medications}; Allergies: {allergies}
        A: Clinical findings noted - {findings}
        P: Treatment plan will be determined following radiographic review.
        """
        st.text_area("Generated SOAP Note", value=soap_note, height=300)

with tabs[1]:
    st.header("🩻 Radiograph Analyzer (GPT Vision)")
    uploaded_image = st.file_uploader("Upload Radiograph (JPG/PNG)", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Radiograph", use_column_width=True)
        if st.button("Analyze with GPT Vision"):
            st.info("🔍 GPT-4 Vision analysis placeholder. Connect to API for real analysis.")
            # Placeholder response for demo
            st.markdown("**Findings:** No periapical radiolucencies noted. Marginal bone levels WNL.")

with tabs[2]:
    st.header("📄 PDF & Chart Uploader (OCR/NLP)")
    uploaded_pdf = st.file_uploader("Upload PDF Document", type=["pdf"])
    if uploaded_pdf:
        pdf_path = f"temp_{uploaded_pdf.name}"
        with open(pdf_path, "wb") as f:
            f.write(uploaded_pdf.read())
        doc = fitz.open(pdf_path)
        text_output = ""
        for page in doc:
            text_output += page.get_text()
        st.text_area("Extracted Text", value=text_output, height=300)
        os.remove(pdf_path)

with tabs[3]:
    st.header("📑 Consent & Education Generator")
    procedure = st.text_input("Procedure Name")
    language = st.selectbox("Select Language", ["English", "Spanish", "Russian", "Haitian Creole"])
    if st.button("Generate Consent Form"):
        st.markdown(f"**Consent for {procedure}** ({language})")
        st.markdown(f"- Risks of not proceeding: infection, tooth loss, worsening condition.")
        st.markdown(f"- Patient was informed of risks, benefits, and alternatives including doing nothing.")
        st.markdown("✅ Patient agreed and provided verbal/written consent.")

with tabs[4]:
    st.header("⚖️ Compliance Auditor")
    st.write("Reviews your SOAP note for legal phrases and insurance compliance.")
    note_input = st.text_area("Paste SOAP Note Here")
    if st.button("Audit Note"):
        if all(x in note_input.lower() for x in ["patient was informed", "risks", "benefits", "alternative"]):
            st.success("✅ Note includes required legal disclosures.")
        else:
            st.error("⚠️ Note missing legal phrasing or risk disclosure.")
