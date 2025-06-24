
import streamlit as st
import json
import openai
import fitz  # for PDFs
from PIL import Image

from generate_soap_note import generate_soap_note
from validate_treatment_plan import validate_treatment_plan

st.set_page_config(page_title="Dental Note Analyzer", layout="wide")
st.title("🦷 Dental Note Analyzer – Modules 1 & 2")

# Sidebar nav
tab = st.sidebar.radio("Select Module", ["📝 SOAP Note Generator", "📋 Treatment Plan Validator"])

if tab == "📝 SOAP Note Generator":
    st.header("Module 1: Smart SOAP Note Generator")

    uploaded_chart = st.file_uploader("Upload patient JSON chart", type=["json"], key="chart")
    patient_data = json.load(uploaded_chart) if uploaded_chart else None

    uploaded_perio = st.file_uploader("Upload perio chart JSON", type=["json"], key="perio")
    perio_data = json.load(uploaded_perio) if uploaded_perio else None

    uploaded_odo = st.file_uploader("Upload odontogram JSON", type=["json"], key="odo")
    odontogram_data = json.load(uploaded_odo) if uploaded_odo else None

    uploaded_docs = st.file_uploader("Upload documents (PDFs)", accept_multiple_files=True, type=["pdf"])
    document_texts = []
    if uploaded_docs:
        for doc in uploaded_docs:
            text = ""
            with fitz.open(stream=doc.read(), filetype="pdf") as pdf:
                for page in pdf:
                    text += page.get_text()
            st.markdown(f"**Extracted from {doc.name}:**")
            st.text(text.strip())
            document_texts.append(text.strip())

    uploaded_images = st.file_uploader("Upload radiographs (JPG/PNG)", accept_multiple_files=True, type=["jpg", "jpeg", "png"])
    radiograph_findings = []
    if uploaded_images:
        for img_file in uploaded_images:
            image = Image.open(img_file)
            st.image(image, caption=f"Uploaded: {img_file.name}", use_column_width=True)
            prompt = """
            You are a dental radiologist AI. Analyze this dental radiograph and provide:
            1. Signs of decay, bone loss, infections, or abnormalities
            2. Tooth numbers involved (if visible)
            3. Signs of prior treatment (implants, crowns, root canals)
            4. Overall impression
            """
            response = openai.ChatCompletion.create(
                model="gpt-4-vision-preview",
                messages=[
                    {"role": "user", "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_file.getvalue().hex()}"}}
                    ]}
                ],
                max_tokens=800
            )
            finding = response.choices[0].message["content"]
            st.markdown(f"**GPT-4 Vision Analysis for {img_file.name}:**")
            st.write(finding)
            radiograph_findings.append(finding)

    if patient_data and st.button("Generate SOAP Note"):
        soap_note = generate_soap_note(patient_data, radiograph_findings, perio_data, odontogram_data, document_texts)
        st.subheader("Generated SOAP Note")
        st.text_area("SOAP Note", soap_note, height=400)

elif tab == "📋 Treatment Plan Validator":
    st.header("Module 2: AI Treatment Plan Validator")

    chart = st.file_uploader("Upload patient chart JSON", type=["json"], key="chart2")
    chart_data = json.load(chart) if chart else None

    plan = st.file_uploader("Upload treatment plan JSON", type=["json"], key="plan")
    treatment_plan = json.load(plan) if plan else None

    odo = st.file_uploader("Upload odontogram JSON (optional)", type=["json"], key="odo2")
    odo_data = json.load(odo) if odo else None

    perio = st.file_uploader("Upload perio chart JSON (optional)", type=["json"], key="perio2")
    perio_data = json.load(perio) if perio else None

    docs = st.file_uploader("Upload extracted documents or notes JSON (optional)", type=["json"], key="docs2")
    doc_data = json.load(docs) if docs else []

    if chart_data and treatment_plan and st.button("Validate Treatment Plan"):
        result = validate_treatment_plan(chart_data, treatment_plan, odo_data, perio_data, doc_data)
        st.subheader("Validation Results")
        st.text_area("Validation Output", result, height=500)
