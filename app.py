
import streamlit as st
from openai import OpenAI

# Secure API Key Access
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="BrightBite - Dental Note Analyzer", layout="wide")

st.title("🧠🦷 BrightBite - Dental Note Analyzer")

# Define tabs
tabs = st.tabs(["Patient Summary", "SOAP Note Generator", "Radiograph Analyzer", 
                "Treatment Plan Validator", "Chairside Diagnostic Assistant", 
                "Consent Generator", "Compliance Auditor"])

with tabs[0]:
    st.header("🧾 Patient Summary")
    st.write("Displays demographic data, medical alerts, conditions, allergies, etc.")

with tabs[1]:
    st.header("📋 Smart SOAP Note Generator")
    st.write("Automatically creates formal, legal-ready notes using all patient data.")

with tabs[2]:
    st.header("🩻 Radiograph Time-Series Analyzer")
    st.write("Upload and compare radiographs using GPT Vision to detect progression.")

with tabs[3]:
    st.header("🛠️ Treatment Plan Validator")
    st.write("Checks for inconsistencies and offers evidence-based recommendations.")

with tabs[4]:
    st.header("🪥 Chairside Diagnostic Assistant")
    st.write("Live interpretation of findings, perio chart, and odontogram context.")

with tabs[5]:
    st.header("📑 Consent & Education Generator")
    st.write("Produces multilingual consent forms with animated patient education.")

with tabs[6]:
    st.header("⚖️ Legal & Insurance Compliance Auditor")
    st.write("Reviews notes for risk flags, missing documentation, and coding gaps.")
