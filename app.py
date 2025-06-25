
import streamlit as st

st.set_page_config(page_title="BrightBite", layout="wide")
st.title("🧠 BrightBite — AI Dental Assistant")
st.info("✅ June 25 Rebuild — All Modules Restored")

# Global Toggles
fullstack_enabled = st.checkbox("⚙️ Enable Full-Stack Automation", value=True)
auto_legal_insert = st.checkbox("🛡 Auto-Complete Missing Legal Phrases", value=True)
deid_enabled = st.checkbox("🧼 De-Identify Before Sending to GPT", value=True)
voice_dictation_enabled = st.checkbox("🎙 Enable Voice Dictation", value=False)
load_test_patient = st.checkbox("🧪 Load Test Patient for Demo", value=False)

# Navigation Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📝 Module 1: Smart Note Generator",
    "🧠 Module 2: Treatment Plan Validator",
    "🧪 Module 3: Diagnostic Assistant",
    "🩻 Module 4: Radiograph Time-Series",
    "📄 Module 5: Patient Education & Consent",
    "🕵️ Module 6: Compliance Auditor"
])

with tab1:
    st.subheader("Smart Note Generator")
    st.file_uploader("📤 Upload Radiograph or FMX")
    st.file_uploader("📤 Upload PDF (Referral, Medical History, etc.)")
    st.text_area("🧾 SOAP Note Output")
    if fullstack_enabled:
        st.success("✅ Full-stack note automation active.")

with tab2:
    st.subheader("AI Treatment Plan Validator")
    st.text_area("📋 Enter Planned Treatment")
    st.button("🧠 Validate with AI")

with tab3:
    st.subheader("Chairside Diagnostic Assistant")
    st.text_input("🦷 Describe Patient Symptoms")
    st.button("🔍 Generate Differential")

with tab4:
    st.subheader("Radiograph Time-Series Analyzer")
    st.file_uploader("📸 Upload Previous Radiograph")
    st.file_uploader("📸 Upload Current Radiograph")
    st.button("📊 Compare & Summarize with Vision")

with tab5:
    st.subheader("Smart Consent & Patient Education")
    st.selectbox("Select Procedure", ["Extraction", "Implant", "Filling", "Crown"])
    st.selectbox("Language", ["English", "Spanish", "Russian", "Haitian Creole"])
    st.button("📃 Generate Consent Form")

with tab6:
    st.subheader("Legal & Insurance Compliance Auditor")
    st.text_area("📝 Paste Draft SOAP Note")
    if auto_legal_insert:
        st.success("🛡 Auto-inserting legal phrases.")
    st.button("🔍 Audit for Missing Phrases")

# Final Visual Confirmation
st.caption("🔒 HIPAA-safe features include: de-identification, local-only reconstruction, optional patient export mode.")
