import openai
import streamlit as st
from PIL import Image
import io
import random
from fpdf import FPDF
import os

# Configure OpenAI API key using environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Sample example patients
example_patients = {
    "John Doe": {
        "patient_name": "John Doe",
        "procedures": "Root canal treatment on #46",
        "perio_summary": "Healthy",
        "radiograph_findings": "Deep decay on #46 close to the pulp",
        "other_notes": "Ibuprofen 400mg prescribed for pain. Educated on regular check-ups.",
        "note_format": "SOAP"
    },
    "Jane Smith": {
        "patient_name": "Jane Smith",
        "procedures": "Scaling and root planing",
        "perio_summary": "Periodontitis with generalized bleeding on probing",
        "radiograph_findings": "Bone loss in posterior regions",
        "other_notes": "Prescribed Chlorhexidine. Educated on diabetes and periodontal health.",
        "note_format": "SOAP"
    },
    "Emily Nguyen": {
        "patient_name": "Emily Nguyen",
        "procedures": "Veneers for anterior teeth",
        "perio_summary": "Healthy",
        "radiograph_findings": "No abnormalities",
        "other_notes": "Referred for cosmetic consultation. Educated on veneer maintenance.",
        "note_format": "Narrative"
    }
}

def simulate_image_interpretation():
    dummy_findings = [
        "Radiolucent lesion on distal root of #19 indicating possible periapical abscess.",
        "Horizontal bone loss observed on mandibular posterior teeth.",
        "Impacted third molar #32 with mesioangular orientation.",
        "Radiopacity in maxillary sinus region suggestive of sinusitis.",
        "Vertical bone defect between teeth #3 and #4.",
        "Generalized calculus deposits evident on bitewing radiographs."
    ]
    return random.choice(dummy_findings)

def generate_radiograph_interpretation(radiograph_findings):
    prompt = f"""
    You are a dental radiology assistant. Interpret the following radiographic findings and write detailed, clinically relevant interpretations in dental chart note format.

    Radiograph Findings: {radiograph_findings}

    Output a paragraph suitable for a dental clinical note.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert dental radiologist assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

def generate_clinical_note(patient_name, procedures, perio_summary, radiograph_findings, other_notes, note_format):
    interpreted_radiographs = generate_radiograph_interpretation(radiograph_findings)
    prompt = f"""
    Generate a dental clinical note in {note_format} format based on the following input:

    Patient: {patient_name}
    Procedures performed today: {procedures}
    Periodontal summary: {perio_summary}
    Radiographic interpretation: {interpreted_radiographs}
    Additional notes: {other_notes}

    Return the output in a clear, readable format suitable for clinical documentation.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert dental clinical documentation assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

def export_note_to_pdf(note_text, filename="dental_note.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in note_text.split('\n'):
        pdf.multi_cell(0, 10, line)
    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output

# Streamlit UI
st.title("🦷 AI-Powered Dental Note Generator with Radiograph Interpretation")

# Example patient selector
example_selection = st.selectbox("Use Example Patient Data", ["None"] + list(example_patients.keys()))

def get_example_data(name):
    return example_patients.get(name, {
        "patient_name": "",
        "procedures": "",
        "perio_summary": "",
        "radiograph_findings": "",
        "other_notes": "",
        "note_format": "SOAP"
    })

example_data = get_example_data(example_selection)

with st.form("note_form"):
    patient_name = st.text_input("Patient Name", value=example_data["patient_name"])
    procedures = st.text_area("Procedures Completed Today", value=example_data["procedures"])
    perio_summary = st.text_area("Periodontal Summary", value=example_data["perio_summary"])
    radiograph_findings = st.text_area("Radiograph Findings (Raw Observations or Simulated Data)", value=example_data["radiograph_findings"])
    uploaded_image = st.file_uploader("Upload Today's Radiograph Image (Mock Upload)", type=["jpg", "png", "jpeg"])
    auto_audit = st.checkbox("Auto-interpret uploaded radiograph (simulated)")
    other_notes = st.text_area("Other Observations or Notes", value=example_data["other_notes"])
    note_format = st.radio("Select Note Format", ["SOAP", "Narrative"], index=0 if example_data["note_format"] == "SOAP" else 1)
    submitted = st.form_submit_button("Generate Note")

if submitted:
    with st.spinner("Generating clinical note with radiograph interpretation..."):
        if uploaded_image:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Radiograph", use_column_width=True)
            if auto_audit:
                radiograph_findings = simulate_image_interpretation()
                st.success(f"Simulated auto-interpretation: {radiograph_findings}")
            else:
                st.info("Note: Automatic image interpretation is currently simulated. Future versions will analyze the image directly.")
        note = generate_clinical_note(patient_name, procedures, perio_summary, radiograph_findings, other_notes, note_format)
        st.subheader("Generated Clinical Note")
        st.code(note, language='markdown')
        pdf_data = export_note_to_pdf(note)
        st.download_button(
            label="📄 Download Note as PDF",
            data=pdf_data,
            file_name="dental_note.pdf",
            mime="application/pdf"
        )
