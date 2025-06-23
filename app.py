
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
        with st.expander("🧍 Basic Info"):
            st.json(data.get("basic_info", {}))

        with st.expander("💳 Insurance Info"):
            st.json(data.get("insurance_info", {}))

        with st.expander("👨‍⚕️ Provider Info"):
            st.json(data.get("provider_info", {}))

        with st.expander("📅 Appointment History"):
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
            # Placeholder for smart logic
            st.warning("Note generation logic not implemented yet. Coming soon!")

    except json.JSONDecodeError:
        st.error("Invalid JSON file. Please upload a properly formatted file.")
else:
    st.warning("Please upload a patient JSON file to begin.")
