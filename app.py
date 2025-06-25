
import streamlit as st
from openai import OpenAI
import base64
from PIL import Image
import fitz  # PyMuPDF
import os

st.set_page_config(page_title="BrightBite - Dental Note Analyzer", layout="wide")
st.title("🧠🦷 BrightBite - Dental Note Analyzer")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# === De-ID Utilities ===
def deidentify(text):
    replacements = {"Patient A": "John Smith", "[DOB]": "01/01/1980"}
    text = text.replace("John Smith", "Patient A").replace("01/01/1980", "[DOB]")
    return text, replacements

def reidentify(text, replacements):
    for fake, real in replacements.items():
        text = text.replace(fake, real)
    return text

deid_enabled = st.checkbox("🛡 De-identify before sending to GPT", value=True)

# === Core Input Section ===
with st.expander("📋 Patient Info & Clinical Inputs", expanded=True):
    name = st.text_input("Patient Name", value="John Smith")
    dob = st.text_input("DOB", value="01/01/1980")
    history = st.text_area("Medical History / Subjective")
    findings = st.text_area("Clinical Findings / Objective")
    diagnosis = st.text_area("Assessment")
    treatment = st.text_area("Planned Treatment")

# === Optional PDF Upload ===
with st.expander("📄 Upload PDF (Optional)"):
    uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])
    parsed_text = ""
    if uploaded_pdf:
        pdf_path = f"temp_{uploaded_pdf.name}"
        with open(pdf_path, "wb") as f:
            f.write(uploaded_pdf.read())
        doc = fitz.open(pdf_path)
        for page in doc:
            parsed_text += page.get_text()
        os.remove(pdf_path)

# === Optional Radiograph Uploads ===
with st.expander("🩻 Upload & Compare Radiographs"):
    old_xray = st.file_uploader("Previous Radiograph", type=["jpg", "jpeg", "png"], key="old_xray")
    new_xray = st.file_uploader("Current Radiograph", type=["jpg", "jpeg", "png"], key="new_xray")
    xray_summary = ""

    if old_xray and new_xray and st.button("🔍 Analyze Radiographs", key="analyze_rads"):
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
            xray_summary = response.choices[0].message.content
            st.markdown("### 🧠 Radiograph Comparison Result")
            st.markdown(xray_summary)
        except Exception as e:
            st.error(f"Vision error: {e}")

# === Consent Generator ===
with st.expander("📑 Consent Generator"):
    procedure = st.text_input("Procedure", key="consent_proc")
    language = st.selectbox("Language", ["English", "Spanish", "Russian", "Haitian Creole"], key="lang_sel")
    consent_text = ""
    if st.button("Generate Consent"):
        consent_text = f"""Consent for {procedure} ({language})
- Risks: infection, pain, failure.
- Alternatives: doing nothing, other procedures.
- Patient consented after discussion and all questions answered.""" 
        st.text_area("Consent Output", value=consent_text, height=200)

# === Compliance Auditor ===
with st.expander("⚖️ Compliance Auditor"):
    note_to_audit = st.text_area("Paste SOAP Note to Audit")
    if st.button("Audit Note"):
        flags = []
        if "risks" not in note_to_audit.lower(): flags.append("Missing risk disclosure")
        if "alternative" not in note_to_audit.lower(): flags.append("Missing alternative discussion")
        if "consent" not in note_to_audit.lower(): flags.append("Missing consent confirmation")
        if flags:
            for flag in flags:
                st.error(f"⚠️ {flag}")
        else:
            st.success("✅ All legal/compliance phrases present.")

# === Full Note Generator ===
if st.button("📝 Generate Full SOAP Note"):
    base_note = f"S: {history}\nO: {findings}\nA: {diagnosis}\nP: {treatment}"
    if parsed_text:
        base_note += f"\n\n[Document Notes]\n{parsed_text}"
    if xray_summary:
        base_note += f"\n\n[Radiograph Summary]\n{xray_summary}"
    if consent_text:
        base_note += f"\n\n[Consent]\n{consent_text}"

    if deid_enabled:
        base_note, replacements = deidentify(base_note)
        st.info("PHI removed before GPT processing.")

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "Format this into a formal dental SOAP note."},
                      {"role": "user", "content": base_note}],
            max_tokens=800
        )
        output = response.choices[0].message.content
        if deid_enabled:
            output = reidentify(output, replacements)
        st.text_area("🧾 Final SOAP Note", value=output, height=400)
    except Exception as e:
        st.error(f"GPT error: {e}")
