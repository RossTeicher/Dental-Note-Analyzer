
import streamlit as st
import openai
import json
import fitz  # PyMuPDF
from PIL import Image
from generate_soap_note import generate_soap_note

st.title("Dental Note Analyzer – Full Mock (PDF + Perio + Odontogram + Radiographs)")

# Upload patient chart
uploaded_chart = st.file_uploader("Upload patient JSON chart", type=["json"])
patient_data = json.load(uploaded_chart) if uploaded_chart else None

# Upload perio chart
uploaded_perio = st.file_uploader("Upload perio chart JSON", type=["json"])
perio_data = json.load(uploaded_perio) if uploaded_perio else None

# Upload odontogram
uploaded_odo = st.file_uploader("Upload odontogram JSON", type=["json"])
odontogram_data = json.load(uploaded_odo) if uploaded_odo else None

# Upload radiographs
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

# Upload PDF documents
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

# Generate SOAP note
if patient_data and st.button("Generate SOAP Note"):
    soap_note = generate_soap_note(
        patient_data,
        radiograph_findings,
        perio_data,
        odontogram_data,
        document_texts
    )
    st.subheader("Generated SOAP Note")
    st.text_area("SOAP Note", soap_note, height=400)
