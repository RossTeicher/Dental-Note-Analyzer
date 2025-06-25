
import streamlit as st

st.set_page_config(page_title="BrightBite", layout="wide")

st.title("🦷 BrightBite - AI Dental Assistant")

# Sidebar toggles
st.sidebar.header("Settings")
deid_enabled = st.sidebar.checkbox("De-identify Before GPT")
fullstack_enabled = st.sidebar.checkbox("Full Stack Automation")
consent_enabled = st.sidebar.checkbox("Include Consent in Plan")
voice_enabled = st.sidebar.checkbox("Enable Voice Dictation")

# Module Tabs
tabs = st.tabs(["Smart Note Generator", "Treatment Plan Validator", "Chairside Diagnostic Assistant",
                "Radiograph Time-Series Analyzer", "Smart Patient Education", "Compliance Auditor"])

with tabs[0]:
    st.subheader("Smart Note Generator")
    st.write("This module generates SOAP notes with all available patient data.")
    uploaded_file = st.file_uploader("Upload Radiograph", type=["jpg", "png", "jpeg"])
    uploaded_pdf = st.file_uploader("Upload Patient PDF", type=["pdf"])
    if st.button("Run Full Stack Automation"):
        st.success("Full stack automation triggered. (Simulated)")
        if deid_enabled:
            st.info("De-identification enabled.")
        if consent_enabled:
            st.info("Consent form included.")
        if voice_enabled:
            st.info("Voice dictation activated.")

with tabs[1]:
    st.subheader("AI Treatment Plan Validator")
    st.write("Validate existing or proposed treatment plans with AI.")

with tabs[2]:
    st.subheader("Chairside Diagnostic Assistant")
    st.write("Real-time diagnostic support for dental findings.")

with tabs[3]:
    st.subheader("Radiograph Time-Series Analyzer")
    st.write("Upload past and current X-rays for change tracking.")

with tabs[4]:
    st.subheader("Smart Patient Education & Consent Generator")
    st.write("Multilingual and risk-stratified education materials.")

with tabs[5]:
    st.subheader("Legal & Insurance Compliance Auditor")
    st.write("Audit SOAP notes for legal and insurance completeness.")
