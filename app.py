import streamlit as st
import json

st.set_page_config(page_title="Dental Note Analyzer", layout="centered")

st.title("🦷 Dental Note Analyzer")
st.subheader("Module 1: Smart Note Generator")
st.markdown("This module will use patient data and clinical findings to generate legally sound SOAP notes.")
st.info("Upload patient data or connect to a database to begin generating notes. (Open Dental integration coming soon!)")

uploaded_file = st.file_uploader("Upload Patient JSON File", type=["json"])
if uploaded_file:
    try:
        patient_data = json.load(uploaded_file)
        st.success("Patient data loaded successfully!")

        # Simulate note generation (SOAP)
        subjective = patient_data.get("subjective", "No subjective findings provided.")
        objective = patient_data.get("objective", "No objective findings provided.")
        assessment = patient_data.get("assessment", "No assessment provided.")
        plan = patient_data.get("plan", "No treatment plan provided.")

        st.markdown("### 📄 Generated SOAP Note")
        st.code(f'''
Subjective:
{subjective}

Objective:
{objective}

Assessment:
{assessment}

Plan:
{plan}
        ''', language="markdown")

        st.download_button("Download SOAP Note as .txt", f'''
Subjective:\n{subjective}\n
Objective:\n{objective}\n
Assessment:\n{assessment}\n
Plan:\n{plan}
        ''', file_name="soap_note.txt")
    except Exception as e:
        st.error(f"Failed to read file: {e}")

st.markdown("---")
st.subheader("Coming Soon")
st.markdown("- 📸 Radiograph AI Analysis\n- 🔗 Direct EHR Integration\n- 📑 Auto-export to PDF and Clinical Records")