
import streamlit as st
import json
import openai
import fitz  # for PDFs
from PIL import Image

from generate_soap_note import generate_soap_note
from validate_treatment_plan import validate_treatment_plan

st.set_page_config(page_title="Dental Note Analyzer", layout="wide")
st.title("🦷 Dental Note Analyzer – Unified App")

# Main UI with tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 SOAP Note Generator", "📋 Treatment Plan Validator", "🧠 Chairside Diagnostic Assistant", "📸 Radiograph Time-Series Analyzer", "📄 Patient Education & Consent"])

with tab1:
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

with tab2:
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

with tab3:
    st.header("Module 3: Chairside Diagnostic Assistant")

    chart3 = st.file_uploader("Upload patient chart JSON", type=["json"], key="chart3")
    chart_data = json.load(chart3) if chart3 else None

    odo3 = st.file_uploader("Upload odontogram JSON", type=["json"], key="odo3")
    odo_data = json.load(odo3) if odo3 else None

    perio3 = st.file_uploader("Upload perio chart JSON", type=["json"], key="perio3")
    perio_data = json.load(perio3) if perio3 else None

    docs3 = st.file_uploader("Upload clinical notes or referrals JSON", type=["json"], key="docs3")
    doc_data = json.load(docs3) if docs3 else []

    xrays3 = st.file_uploader("Upload radiographs (JPG/PNG)", accept_multiple_files=True, type=["jpg", "jpeg", "png"], key="xray3")
    radiograph_findings = []
    if xrays3:
        for img_file in xrays3:
            image = Image.open(img_file)
            st.image(image, caption=f"Uploaded: {img_file.name}", use_column_width=True)
            prompt = """
            You are a dental radiologist AI. Please analyze this image and summarize the diagnostic findings.
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
            result = response.choices[0].message["content"]
            radiograph_findings.append(result)
            st.markdown(f"**Radiograph Analysis for {img_file.name}:**")
            st.write(result)

    if chart_data and st.button("Run Chairside Diagnostic Analysis"):
        from diagnostic_assistant import generate_diagnostic_summary
        output = generate_diagnostic_summary(chart_data, odo_data, perio_data, doc_data, radiograph_findings)
        st.subheader("Diagnostic Assistant Output")
        st.text_area("Tooth-by-Tooth Diagnostic Summary", output, height=500)

with tab4:
    st.header("Module 4: Radiograph Time-Series Analyzer")

    uploaded_rads = st.file_uploader("Upload Radiographs (JPG/PNG) – oldest to newest", type=["jpg", "jpeg", "png"], accept_multiple_files=True, key="rads4")
    rad_labels = []
    labeled_images = []

    if uploaded_rads:
        st.markdown("### 🗂️ Label each radiograph")
        for i, img_file in enumerate(uploaded_rads):
            col1, col2 = st.columns([1, 3])
            with col1:
                label = st.text_input(f"Label for {img_file.name} (e.g. 'Before', 'After', '06-01-2024')", key=f"label_{i}")
                rad_labels.append(label)
            with col2:
                st.image(img_file, caption=f"Uploaded: {img_file.name}", use_column_width=True)
            labeled_images.append((img_file, label))

    if labeled_images and st.button("🧠 Compare Radiographs"):
        from radiograph_time_series import compare_radiographs
        summary = compare_radiographs(labeled_images)
        st.subheader("Radiographic Comparison Summary")
        st.text_area("Radiologist-style Report", summary, height=500)

with tab5:
    st.header("Module 5: Smart Patient Education & Consent Generator")

    chart5 = st.file_uploader("Upload patient chart JSON", type=["json"], key="chart5")
    chart_data = json.load(chart5) if chart5 else None

    plan5 = st.file_uploader("Upload treatment plan JSON", type=["json"], key="plan5")
    treatment_plan = json.load(plan5) if plan5 else None

    language = st.selectbox("Select Language for Output", ["English", "Spanish", "Russian", "Haitian Creole"], key="lang5")

    if chart_data and treatment_plan and st.button("🧾 Generate Patient Education + Consent"):
        from patient_education_consent import generate_patient_consent_package
        consent, scary_note, education, video_description = generate_patient_consent_package(chart_data, treatment_plan, language)

        st.subheader("📝 Consent Form")
        st.text_area("Consent Text", consent, height=250)

        st.subheader("⚠️ Scary Note")
        st.text_area("Layman's Risk Explanation", scary_note, height=180)

        st.subheader("📘 Patient Education")
        st.text_area("Simple Summary of Why This Matters", education, height=180)

        st.subheader("🎥 (Mock) AI-Generated Video Summary")
        st.markdown(video_description)

        if st.button("📄 Download PDF Summary"):
            from patient_education_consent_pdf import generate_consent_pdf
            pdf_path = generate_consent_pdf(education, scary_note)
            st.success("PDF created successfully.")
            st.download_button(label="⬇️ Download Treatment Options PDF", file_name="Treatment_Options_And_Risks.pdf", mime="application/pdf", data=open(pdf_path, "rb").read())

