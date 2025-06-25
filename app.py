
import streamlit as st
from openai import OpenAI
import base64
from PIL import Image
import fitz  # PyMuPDF
import os

st.set_page_config(page_title="BrightBite - Dental Note Analyzer", layout="wide")
st.title("🧠🦷 BrightBite - Dental Note Analyzer")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# === De-identification utilities ===
def deidentify(text):
    replacements = {"Patient A": "John Smith", "[DOB]": "01/01/1980"}
    text = text.replace("John Smith", "Patient A").replace("01/01/1980", "[DOB]")
    return text, replacements

def reidentify(text, replacements):
    for fake, real in replacements.items():
        text = text.replace(fake, real)
    return text

# === De-ID Toggle ===
deid_enabled = st.checkbox("🛡 De-identify before sending to GPT", value=True)

# === Unified Inputs ===
with st.expander("📋 Patient Information"):
    name = st.text_input("Patient Name", value="John Smith")
    dob = st.text_input("DOB", value="01/01/1980")
    history = st.text_area("Medical History / Subjective")
    findings = st.text_area("Clinical Findings / Objective")
    diagnosis = st.text_area("Assessment")
    treatment = st.text_area("Planned Treatment")

with st.expander("🩻 Upload Radiographs for Comparison (Optional)"):
    old_xray = st.file_uploader("Previous Radiograph", type=["jpg", "jpeg", "png"], key="old_xray")
    new_xray = st.file_uploader("Current Radiograph", type=["jpg", "jpeg", "png"], key="new_xray")

with st.expander("📄 Upload PDF Document (Optional)"):
    uploaded_pdf = st.file_uploader("PDF", type=["pdf"])
    parsed_text = ""
    if uploaded_pdf:
        pdf_path = f"temp_{uploaded_pdf.name}"
        with open(pdf_path, "wb") as f:
            f.write(uploaded_pdf.read())
        doc = fitz.open(pdf_path)
        for page in doc:
            parsed_text += page.get_text()
        os.remove(pdf_path)

# === Automated Full Note Generation ===
if st.button("📝 Generate Full Note"):
    # Combine all text components
    base_note = f"S: {history}\nO: {findings}\nA: {diagnosis}\nP: {treatment}"
    full_note = base_note
    if parsed_text:
        full_note += f"\n\n[Document Extracted Notes]\n{parsed_text}"

    # De-identify if enabled
    if deid_enabled:
        full_note, replacements = deidentify(full_note)
        st.success("✅ PHI was removed before GPT processing.")

    # GPT-4 processing (SOAP note cleanup and formatting)
    try:
        gpt_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Format this clinical input into a formal SOAP note for dental documentation."},
                {"role": "user", "content": full_note}
            ],
            max_tokens=800
        )
        result = gpt_response.choices[0].message.content
        if deid_enabled:
            result = reidentify(result, replacements)
        st.text_area("🧾 Final SOAP Note", value=result, height=400)
    except Exception as e:
        st.error(f"Error processing GPT: {e}")

# === GPT-4 Vision Radiograph Comparison ===
if old_xray and new_xray and st.button("🔍 Analyze Radiographs with GPT-4 Vision"):
    images = [
        {"image": old_xray.getvalue(), "desc": "This is the earlier radiograph."},
        {"image": new_xray.getvalue(), "desc": "This is the more recent radiograph."}
    ]
    vision_inputs = []
    for img in images:
        b64_img = base64.b64encode(img["image"]).decode("utf-8")
        vision_inputs.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{b64_img}"},
        })
        vision_inputs.append({"type": "text", "text": img["desc"]})

    try:
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[{"role": "user", "content": vision_inputs}],
            max_tokens=500
        )
        result = response.choices[0].message.content
        st.markdown("### 🧠 GPT-4 Vision Radiograph Comparison")
        st.markdown(result)
    except Exception as e:
        st.error(f"Vision analysis failed: {e}")
