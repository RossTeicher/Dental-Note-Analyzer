
import streamlit as st
import openai
from PIL import Image
from generate_soap_note import generate_soap_note

st.title("Dental Note Analyzer – Demo Mode (Mock Data)")

# Mock patient data in place of database connection
patient_data = {
    "core_info": {
        "Name": "Jane Doe",
        "DOB": "1992-06-15",
        "Gender": "Female",
        "Status": "Active"
    },
    "appointments": [
        {"Date": "2025-06-21", "Type": "Recall", "Provider": "Dr. Smith"},
    ],
    "medications": [
        {"MedName": "Lisinopril", "Notes": "10mg daily"}
    ],
    "allergies": [
        {"Allergy": "Penicillin"}
    ],
    "conditions": [
        {"Condition": "Hypertension"}
    ],
    "procedures": [
        {"Code": "D0150", "Tooth": "", "Date": "2025-06-21"},
        {"Code": "D1110", "Tooth": "", "Date": "2025-06-21"},
        {"Code": "D2392", "Tooth": "#30", "Date": "2025-06-21"},
        {"Code": "D2740", "Tooth": "#8", "Date": "2025-06-21"}
    ],
    "notes": [
        {"Date": "2025-06-21", "Note": "Patient reports sensitivity on lower right molar."}
    ]
}

# Radiograph upload
uploaded_images = st.file_uploader(
    "Upload today's radiographs (JPG/PNG only)",
    accept_multiple_files=True,
    type=["jpg", "jpeg", "png"]
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

# SOAP generation
if st.button("Generate SOAP Note"):
    soap_note = generate_soap_note(patient_data, radiograph_findings)
    st.subheader("Generated SOAP Note")
    st.text_area("SOAP Note", soap_note, height=400)
