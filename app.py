import streamlit as st
import json
import os

st.set_page_config(page_title="Dental Note Analyzer", layout="centered")
st.title("🦷 Dental Note Analyzer")
st.subheader("Module 1: Smart Note Generator")

st.info("This module will use patient data and clinical findings to generate legally sound, deposition-grade SOAP notes.")

uploaded_file = st.file_uploader("Upload Full Patient Profile (.json)", type=["json"])

if uploaded_file:
    try:
        data = json.load(uploaded_file)

        st.success("Patient data uploaded successfully.")

        # Display core data categories
        with st.expander("🧝 Basic Info"):
            st.json(data.get("basic_info", {}))

        with st.expander("💳 Insurance Info"):
            st.json(data.get("insurance_info", {}))

        with st.expander("👨‍⚕️ Provider Info"):
            st.json(data.get("provider_info", {}))

        with st.expander("🗕 Appointment History"):
            st.json(data.get("appointments", []))

        with st.expander("🚨 Allergies & Medical Alerts"):
            st.json(data.get("alerts", {}))

        with st.expander("💊 Medications & Conditions"):
            st.json({
                "Medications": data.get("medications", []),
                "Conditions": data.get("medical_conditions", [])
            })

        with st.expander("📋 Treatment Plans"):
            st.json({
                "Ongoing": data.get("ongoing_treatment", []),
                "Planned": data.get("planned_procedures", [])
            })

        with st.expander("✅ Completed Procedures"):
            st.json(data.get("completed_procedures", []))

        with st.expander("📝 Past Notes"):
            st.json(data.get("notes", []))

        with st.expander("📸 Radiographs"):
            st.json(data.get("radiographs", []))
            st.caption("(Vision analysis & time-series comparison handled by GPT-vision back-end API)")

        with st.expander("🦷 Perio Charting"):
            st.json(data.get("perio_charting", {}))

        with st.expander("📄 Scanned Documents"):
            st.json(data.get("documents", []))
            st.caption("(OCR + NLP parsing handled in backend)")

        st.divider()
        if st.button("Generate SOAP Note"):
            basic = data.get("basic_info", {})
            conditions = data.get("medical_conditions", [])
            meds = data.get("medications", [])
            alerts = data.get("alerts", {})
            ongoing = data.get("ongoing_treatment", [])
            planned = data.get("planned_procedures", [])
            notes = data.get("notes", [])
            procedures = data.get("completed_procedures", [])

            soap_note = f"""
**Subjective:**
Patient {basic.get('name', 'N/A')} presents for evaluation with known conditions: {', '.join(conditions) or 'None reported'}.
Medications: {', '.join(meds) or 'None reported'}.
Medical alerts: {alerts.get('medical_alerts', 'None')} | Allergies: {alerts.get('allergies', 'None')}.

**Objective:**
Radiographs, perio charting, and scanned documents reviewed via AI-supported analysis.
Ongoing treatment: {', '.join([t.get('description', '') for t in ongoing]) or 'None'}.
Completed procedures: {', '.join([p.get('procedure', '') + ' on ' + p.get('date', '') for p in procedures]) or 'None'}.

**Assessment:**
Summarizing 3 most recent notes:
{chr(10).join([note.get('content', '') for note in notes[-3:]]) or 'No recent documentation.'}
AI Risk Stratification: (Coming soon - Legal AI flags abnormal/systemic risks)

**Plan:**
Upcoming procedures: {', '.join([p.get('procedure', '') for p in planned]) or 'None scheduled.'}
Voice dictation: Enabled via toggle (Coming soon)
Legal mode: Active - Notes formatted for deposition-readiness
"""

            st.code(soap_note.strip(), language="markdown")

    except json.JSONDecodeError:
        st.error("Invalid JSON file. Please upload a properly formatted file.")
else:
    st.warning("Please upload a patient JSON file to begin.")