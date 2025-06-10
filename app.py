import streamlit as st
from openai import OpenAI, OpenAIError
import os
from procedure_list import procedures
from lang_map import lang_map
from fpdf import FPDF
import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import tempfile

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("🦷 Multilingual Consent | Analytics | Signature | Animations")

# Sidebar for analytics
st.sidebar.header("📊 Case Acceptance Analytics")
if os.path.exists("case_acceptance_log.csv"):
    df = pd.read_csv("case_acceptance_log.csv", header=None, names=["Timestamp", "Patient", "Procedure", "Language", "Accepted"])
    fig, ax = plt.subplots()
    df['Accepted'].value_counts().plot(kind='bar', ax=ax, title="Case Acceptance Summary")
    st.sidebar.pyplot(fig)

# Main consent generator
st.header("📄 Consent Form Generator")

category = st.selectbox("Select Procedure Category", list(procedures.keys()))
procedure = st.selectbox("Select Specific Procedure", procedures[category])
language = st.selectbox("Select Language", list(lang_map.keys()))
patient_name = st.text_input("Patient Name")
case_accepted = st.radio("Case Accepted?", ["Yes", "No"])
notes = st.text_area("Clinical Summary", "Gingival inflammation noted with bone loss.")
signature = st.text_input("Type Patient Signature")

if st.button("Generate Consent Form"):
    with st.spinner("Creating form..."):
        try:
            prompt = f"""You are a multilingual dental AI assistant. Generate a consent form.

Language: {language}
Procedure: {procedure}
Details: {notes}

Include:
- Procedure description
- Risks/benefits/alternatives
- Post-op care
- Legal disclaimers
- Patient-friendly language
"""

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.choices[0].message.content

            st.text_area(f"{language} Consent Form", content, height=400)

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            for line in content.split("\n"):
                try:
                    pdf.multi_cell(0, 10, line)
                except UnicodeEncodeError:
                    pdf.multi_cell(0, 10, line.encode('latin-1', 'replace').decode('latin-1'))

            if signature:
                pdf.ln(10)
                pdf.cell(0, 10, f"Signature: {signature}", ln=True)

            file_path = os.path.join(tempfile.gettempdir(), f"{patient_name.replace(' ', '_')}_consent.pdf")
            pdf.output(file_path)

            with open(file_path, "rb") as f:
                st.download_button("📥 Download PDF", f, file_name=f"{patient_name}_consent.pdf", mime="application/pdf")

            with open("case_acceptance_log.csv", "a", newline="") as logfile:
                writer = csv.writer(logfile)
                writer.writerow([datetime.now().isoformat(), patient_name, procedure, language, case_accepted])
        except OpenAIError as e:
            st.error(f"OpenAI error: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

# AI Patient Animation Generator
st.header("🎞️ Generate Patient Animation Description")
if st.button("Create Animation Script"):
    try:
        anim_prompt = f"Create a short animation storyboard script to explain the '{procedure}' procedure in {language} for patient education."
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": anim_prompt}]
        )
        st.text_area("📽️ Animation Script", response.choices[0].message.content, height=300)
    except Exception as e:
        st.error(f"Animation generation failed: {e}")
