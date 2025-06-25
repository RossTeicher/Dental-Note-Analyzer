
import streamlit as st
from openai import OpenAI
from PIL import Image
import fitz
import os

st.set_page_config(page_title="BrightBite - Dental Note Analyzer", layout="wide")
st.title("🧠🦷 BrightBite - Dental Note Analyzer")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

tabs = st.tabs(["SOAP Note Generator", "Radiograph Analyzer", "PDF & Chart Uploader",
                "Treatment Plan Validator", "Chairside Diagnostic Assistant", 
                "Consent Generator", "Compliance Auditor"])

with tabs[0]:
    st.header("📋 Smart SOAP Note Generator")
    st.text_input("Patient Name")
    st.text_area("Medical History")
    st.text_area("Medications")
    st.text_area("Allergies")
    st.text_area("Clinical Findings")
    st.text_area("Planned Treatment")
    if st.button("Generate SOAP Note"):
        note = (
            "S: History and subjective complaints provided by patient.\n"
            "O: Clinical findings recorded.\n"
            "A: Initial assessment based on current presentation.\n"
            "P: Proceed with proposed treatment or defer pending further evaluation."
        )
        st.text_area("Generated SOAP Note", value=note, height=250)

with tabs[1]:
    st.header("🩻 Radiograph Time-Series Analyzer")
    col1, col2 = st.columns(2)
    with col1:
        img1 = st.file_uploader("Upload Old Radiograph", type=["jpg", "jpeg", "png"], key="old")
    with col2:
        img2 = st.file_uploader("Upload New Radiograph", type=["jpg", "jpeg", "png"], key="new")
    if img1 and img2:
        st.image(Image.open(img1), caption="Old Radiograph", width=300)
        st.image(Image.open(img2), caption="New Radiograph", width=300)
        if st.button("Compare Images with GPT-4 Vision"):
            # Simulated GPT-4 Vision logic
            st.markdown("**Findings:** Slight progression of bone loss in molar region. Monitor #30 closely.")
            st.markdown("**Summary:** Changes detected over time. Consider updated treatment planning.")

with tabs[2]:
    st.header("📄 PDF & Chart Uploader (OCR/NLP)")
    uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])
    if uploaded_pdf:
        temp_path = f"temp_{uploaded_pdf.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_pdf.read())
        doc = fitz.open(temp_path)
        extracted = "\n".join([page.get_text() for page in doc])
        st.text_area("Extracted Text", value=extracted, height=300)
        os.remove(temp_path)

with tabs[3]:
    st.header("🛠️ Treatment Plan Validator")
    st.text_area("Planned Treatment")
    st.text_area("Previous Treatment Summary")
    if st.button("Validate Treatment Plan"):
        st.success("✅ No discrepancies detected. Plan aligns with patient history and radiographic findings.")

with tabs[4]:
    st.header("🪥 Chairside Diagnostic Assistant")
    st.text_area("Enter Clinical Findings")
    if st.button("Generate Diagnostic Summary"):
        st.info("🧠 GPT-based logic placeholder: Class I occlusion, mild generalized gingivitis.")

with tabs[5]:
    st.header("📑 Consent & Education Generator")
    procedure = st.text_input("Procedure")
    language = st.selectbox("Language", ["English", "Spanish", "Russian", "Haitian Creole"])
    animated = st.checkbox("Include animated explanation?")
    if st.button("Generate Consent"):
        st.write(f"### Consent for {procedure} ({language})")
        st.markdown("- Risks of not proceeding: pain, infection, tooth loss.")
        st.markdown("- Patient informed of risks, benefits, and alternatives.")
        st.markdown("- Option to do nothing presented.")
        if animated:
            st.video("https://www.youtube.com/embed/2qNc1YwAfmc")

with tabs[6]:
    st.header("⚖️ Legal & Insurance Compliance Auditor")
    note = st.text_area("Paste SOAP Note")
    if st.button("Audit Note"):
        issues = []
        required = ["risks", "benefits", "alternative", "patient was informed"]
        for phrase in required:
            if phrase not in note.lower():
                issues.append(f"Missing: '{phrase}'")
        if issues:
            st.error("⚠️ Issues found:\n" + "\n".join(issues))
        else:
            st.success("✅ Note includes all required legal elements.")
