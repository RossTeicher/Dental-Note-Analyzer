
import streamlit as st
import json
import os

st.set_page_config(page_title="Dental Note Analyzer", layout="centered")
st.title("🦷 Dental Note Analyzer")
st.subheader("Module 1: Smart Note Generator")

st.info("This module will use patient data and clinical findings to generate legally sound SOAP notes.")

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

        with st.expander("🦷 Perio Charting"):
            st.json(data.get("perio_charting", {}))

        st.divider()
        if st.button("Generate SOAP Note"):
            basic = data.get("basic_info", {})
            conditions = data.get("medical_conditions", [])
            meds = data.get("medications", [])
            alerts = data.get("alerts", {})
            ongoing = data.get("ongoing_treatment", [])
            planned = data.get("planned_procedures", [])
            notes = data.get("notes", [])

            soap_note = f"""**Subjective:**
Patient {basic.get('name', 'N/A')} presents with known medical conditions: {', '.join(conditions) or 'None reported'}.
Medications include: {', '.join(meds) or 'None reported'}.
Allergies and alerts: {alerts.get('allergies', 'None')} | {alerts.get('medical_alerts', 'None')}.

**Objective:**
Clinical findings from radiographs and perio charting reviewed.
Ongoing treatments: {', '.join([t.get('description', '') for t in ongoing]) or 'None'}.

**Assessment:**
Review of notes and completed procedures supports continuity of care. Past assessments:
{chr(10).join([note.get('content', '') for note in notes[-3:]]) or 'No recent notes available.'}

**Plan:**
Planned procedures include: {', '.join([p.get('procedure', '') for p in planned]) or 'No upcoming procedures scheduled.'}"""

            st.code(soap_note.strip(), language="markdown")

    except json.JSONDecodeError:
        st.error("Invalid JSON file. Please upload a properly formatted file.")
else:
    st.warning("Please upload a patient JSON file to begin.")
