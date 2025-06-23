import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="Dental Note Analyzer", layout="centered")
st.title("🦷 Dental Note Analyzer")
st.subheader("Module 1: Smart Note Generator")

st.info("This module uses patient data to generate legally sound SOAP notes with feedback improvement over time.")

uploaded_file = st.file_uploader("Upload Full Patient Profile (.json)", type=["json"])

# Load past feedback (simple version)
FEEDBACK_LOG = "feedback_log.json"
if os.path.exists(FEEDBACK_LOG):
    with open(FEEDBACK_LOG, "r") as f:
        feedback_history = json.load(f)
else:
    feedback_history = []

if uploaded_file:
    try:
        data = json.load(uploaded_file)
        st.success("Patient data uploaded successfully.")

        # Display core categories
        with st.expander("🧝 Basic Info"): st.json(data.get("basic_info", {}))
        with st.expander("💳 Insurance Info"): st.json(data.get("insurance_info", {}))
        with st.expander("👨‍⚕️ Provider Info"): st.json(data.get("provider_info", {}))
        with st.expander("🗕 Appointment History"): st.json(data.get("appointments", []))
        with st.expander("🚨 Allergies & Medical Alerts"): st.json(data.get("alerts", {}))
        with st.expander("💊 Medications & Conditions"):
            st.json({"Medications": data.get("medications", []), "Conditions": data.get("medical_conditions", [])})
        with st.expander("📋 Treatment Plans"):
            st.json({"Ongoing": data.get("ongoing_treatment", []), "Planned": data.get("planned_procedures", [])})
        with st.expander("✅ Completed Procedures"): st.json(data.get("completed_procedures", []))
        with st.expander("📝 Past Notes"): st.json(data.get("notes", []))
        with st.expander("📸 Radiographs"): st.json(data.get("radiographs", []))
        with st.expander("🦷 Perio Charting"): st.json(data.get("perio_charting", {}))

        st.divider()

        if st.button("Generate SOAP Note"):
            def format_procedure(proc):
                return f"{proc.get('date', '')}: {proc.get('procedure', '')} - {proc.get('details', 'No detail provided')}"

            basic = data.get("basic_info", {})
            conditions, meds, alerts = data.get("medical_conditions", []), data.get("medications", []), data.get("alerts", {})
            ongoing, planned, notes = data.get("ongoing_treatment", []), data.get("planned_procedures", []), data.get("notes", [])

            soap_note = f"""**Subjective:**
Patient {basic.get('name', 'N/A')} presents with conditions: {', '.join(conditions) or 'None reported'}.
Medications: {', '.join(meds) or 'None reported'}.
Alerts: {alerts.get('allergies', 'None')} | {alerts.get('medical_alerts', 'None')}.

**Objective:**
Reviewed radiographs and perio charting. 
Ongoing treatments include: {', '.join([t.get('description', '') for t in ongoing]) or 'None'}.

**Assessment:**
Summarizing recent assessments:
{chr(10).join([note.get('content', '') for note in notes[-3:]]) or 'No prior notes available.'}

**Plan:**
Planned procedures:
{chr(10).join([format_procedure(p) for p in planned]) or 'None scheduled.'}"""

            st.code(soap_note.strip(), language="markdown")

            st.text_input("Optional feedback on this note:", key="feedback_input")
            if st.button("Submit Feedback"):
                user_feedback = st.session_state.get("feedback_input", "")
                feedback_entry = {"timestamp": datetime.now().isoformat(), "feedback": user_feedback, "note": soap_note.strip()}
                feedback_history.append(feedback_entry)
                with open(FEEDBACK_LOG, "w") as f:
                    json.dump(feedback_history, f, indent=2)
                st.success("Feedback submitted and logged. Thanks!")

    except json.JSONDecodeError:
        st.error("Invalid JSON file format.")
else:
    st.warning("Please upload a patient JSON file to begin.")