
import streamlit as st
import openai
import json
from PIL import Image
from generate_soap_note import generate_soap_note

st.title("Dental Note Analyzer – Mock Mode (Chart + Perio + Odontogram + Radiographs)")

# Upload patient chart
uploaded_chart = st.file_uploader("Upload patient JSON chart", type=["json"])
if uploaded_chart:
    try:
        patient_data = json.load(uploaded_chart)
        st.success("Patient chart uploaded.")
        st.json(patient_data)
    except Exception as e:
        st.error(f"Error parsing chart JSON: {e}")
        patient_data = None
else:
    patient_data = None

# Upload perio chart
uploaded_perio = st.file_uploader("Upload perio chart JSON", type=["json"])
if uploaded_perio:
    try:
        perio_data = json.load(uploaded_perio)
        st.success("Perio chart uploaded.")
        st.json(perio_data)
    except Exception as e:
        st.error(f"Error parsing perio chart JSON: {e}")
        perio_data = None
else:
    perio_data = None

# Upload odontogram
uploaded_odo = st.file_uploader("Upload odontogram JSON", type=["json"])
if uploaded_odo:
    try:
        odontogram_data = json.load(uploaded_odo)
        st.success("Odontogram uploaded.")
        st.json(odontogram_data)
    except Exception as e:
        st.error(f"Error parsing odontogram JSON: {e}")
        odontogram_data = None
else:
    odontogram_data = None

# Upload radiographs
uploaded_images = st.file_uploader(
    "Upload radiographs (JPG/PNG)", accept_multiple_files=True, type=["jpg", "jpeg", "png"]
)

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

# SOAP Generation
if patient_data and st.button("Generate SOAP Note"):
    soap_note = generate_soap_note(patient_data, radiograph_findings, perio_data, odontogram_data)
    st.subheader("Generated SOAP Note")
    st.text_area("SOAP Note", soap_note, height=400)
