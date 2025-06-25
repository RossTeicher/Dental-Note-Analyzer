
import streamlit as st

st.set_page_config(page_title="BrightBite", layout="wide")
st.title("🧠🦷 BrightBite - AI Dental Assistant Platform")
st.markdown("Welcome to BrightBite! Choose a module from the sidebar.")

# Import all modules
from module_1_smart_note_generator import run_module_1
from module_2_treatment_validator import run_module_2
from module_3_diagnostic_assistant import run_module_3
from module_4_radiograph_analyzer import run_module_4
from module_5_patient_education import run_module_5
from module_6_compliance_auditor import run_module_6

# Sidebar navigation
selected = st.sidebar.radio("Select Module", [
    "Module 1: Smart Note Generator",
    "Module 2: Treatment Plan Validator",
    "Module 3: Chairside Diagnostic Assistant",
    "Module 4: Radiograph Time-Series Analyzer",
    "Module 5: Patient Education & Consent Generator",
    "Module 6: Legal & Insurance Compliance Auditor"
])

if selected == "Module 1: Smart Note Generator":
    run_module_1()
elif selected == "Module 2: Treatment Plan Validator":
    run_module_2()
elif selected == "Module 3: Chairside Diagnostic Assistant":
    run_module_3()
elif selected == "Module 4: Radiograph Time-Series Analyzer":
    run_module_4()
elif selected == "Module 5: Patient Education & Consent Generator":
    run_module_5()
elif selected == "Module 6: Legal & Insurance Compliance Auditor":
    run_module_6()
