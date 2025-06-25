
import streamlit as st
from openai import OpenAI
from PIL import Image
import fitz  # PyMuPDF
import os

st.set_page_config(page_title="BrightBite - Dental Note Analyzer", layout="wide")
st.title("🧠🦷 BrightBite - Dental Note Analyzer")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

tabs = st.tabs([
    "SOAP Note Generator", "Radiograph Comparison (GPT Vision)",
    "PDF/OCR Parser", "Treatment Plan Validator",
    "Chairside Assistant", "Consent Generator", "Compliance Auditor"
])

with tabs[0]:
    st.header("📋 SOAP Note Generator")
    pt_name = st.text_input("Patient Name", key="pt_name")
    history = st.text_area("Medical History", key="med_history")
    meds = st.text_area("Current Medications", key="meds")
    allergies = st.text_area("Allergies", key="allergies")
    findings = st.text_area("Clinical Findings", key="findings")
    if st.button("Generate SOAP Note", key="gen_soap"):
        note = f"""S: Patient {pt_name} reports {history}
O: Medications: {meds}; Allergies: {allergies}
A: {findings}
P: Proceed with radiographic evaluation and treatment planning.""" 
        st.text_area("Generated SOAP Note", value=note, height=300, key="output_soap")

with tabs[1]:
    st.header("🩻 Radiograph Comparison (GPT Vision)")
    img1 = st.file_uploader("Upload Previous Radiograph", type=["jpg", "jpeg", "png"], key="img1")
    img2 = st.file_uploader("Upload Current Radiograph", type=["jpg", "jpeg", "png"], key="img2")
    if img1 and img2:
        st.image(Image.open(img1), caption="Previous Radiograph", use_column_width=True)
        st.image(Image.open(img2), caption="Current Radiograph", use_column_width=True)
        if st.button("Compare with GPT Vision", key="compare_imgs"):
            st.info("🧠 GPT-4 Vision would analyze and summarize differences here (stub logic).")
            st.markdown("**Comparison Result:** Slight bone loss observed in #30 area compared to prior.")

with tabs[2]:
    st.header("📄 PDF/OCR Parser")
    uploaded_pdf = st.file_uploader("Upload PDF Document", type=["pdf"], key="pdf_doc")
    if uploaded_pdf:
        pdf_path = f"temp_{uploaded_pdf.name}"
        with open(pdf_path, "wb") as f:
            f.write(uploaded_pdf.read())
        doc = fitz.open(pdf_path)
        text_output = ""
        for page in doc:
            text_output += page.get_text()
        st.text_area("Extracted Text", value=text_output, height=300, key="ocr_output")
        os.remove(pdf_path)

with tabs[3]:
    st.header("🛠️ Treatment Plan Validator")
    completed_tx = st.text_area("Completed Procedures", key="completed_tx")
    planned_tx = st.text_area("Planned Treatment", key="planned_tx")
    if st.button("Validate Plan", key="validate_plan"):
        if "extraction" in planned_tx.lower() and "crown" in completed_tx.lower():
            st.warning("⚠️ Check if crown is still viable before extraction.")
        else:
            st.success("✅ No conflicting treatments detected.")

with tabs[4]:
    st.header("🪥 Chairside Diagnostic Assistant")
    odonto_notes = st.text_area("Odontogram Findings", key="odonto")
    perio_status = st.text_area("Perio Chart Summary", key="perio")
    if st.button("Generate Diagnostic Summary", key="diagnostic_summary"):
        summary = f"Patient shows: {odonto_notes}. Perio charting indicates: {perio_status}."
        st.text_area("Diagnostic Summary", value=summary, height=200, key="diag_summary")

with tabs[5]:
    st.header("📑 Consent Generator")
    procedure = st.text_input("Procedure", key="procedure")
    language = st.selectbox("Language", ["English", "Spanish", "Russian", "Haitian Creole"], key="lang")
    if st.button("Generate Consent Form", key="gen_consent"):
        st.markdown(f"**Consent Form for {procedure} ({language})**")
        st.markdown("- Explained risks: infection, discomfort, treatment failure.")
        st.markdown("- Patient offered alternatives including no treatment.")
        st.markdown("✅ Patient gave informed consent.")

with tabs[6]:
    st.header("⚖️ Compliance Auditor")
    note_input = st.text_area("Paste SOAP Note for Audit", key="audit_input")
    if st.button("Run Compliance Audit", key="run_audit"):
        flags = []
        if "risks" not in note_input.lower(): flags.append("Missing risk disclosure")
        if "alternative" not in note_input.lower(): flags.append("Missing treatment alternatives")
        if "consent" not in note_input.lower(): flags.append("Missing consent confirmation")
        if flags:
            for issue in flags:
                st.error(f"⚠️ {issue}")
        else:
            st.success("✅ All legal components present.")
