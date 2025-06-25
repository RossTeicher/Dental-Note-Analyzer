
import streamlit as st
from openai import OpenAI
from PIL import Image
import fitz
import base64
import os

st.set_page_config(page_title="BrightBite - Investor Demo", layout="wide")
st.title("🧠🦷 BrightBite - Dental Note Analyzer — Investor Demo")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- De-ID Setup ---
def deidentify(text):
    replacements = {"Patient A": "John Smith", "[DOB]": "01/01/1980"}
    text = text.replace("John Smith", "Patient A").replace("01/01/1980", "[DOB]")
    return text, replacements

def reidentify(text, replacements):
    for fake, real in replacements.items():
        text = text.replace(fake, real)
    return text

# --- Voice Dictation Toggle (Placeholder UI) ---
st.checkbox("🎙 Enable Voice Dictation (Demo Placeholder)", value=False)

# --- Load Demo Test Patient ---
if st.button("👤 Load Test Patient: John Smith (General Exam)"):
    st.session_state["name"] = "John Smith"
    st.session_state["dob"] = "01/01/1980"
    st.session_state["history"] = "Patient presents for routine dental examination and cleaning."
    st.session_state["meds"] = "Lisinopril 10mg daily"
    st.session_state["allergies"] = "Penicillin"
    st.session_state["findings"] = "Class I occlusion. Mild gingival recession. No visible caries. 1-3mm pockets."
    st.session_state["diagnosis"] = "Generalized mild gingivitis. Good overall oral hygiene."
    st.session_state["treatment"] = "Adult prophy, oral hygiene instruction."

# --- Input Section ---
with st.expander("📋 Patient Data", expanded=True):
    name = st.text_input("Patient Name", value=st.session_state.get("name", ""))
    dob = st.text_input("Date of Birth", value=st.session_state.get("dob", ""))
    history = st.text_area("Subjective (CC/History)", value=st.session_state.get("history", ""))
    meds = st.text_area("Medications", value=st.session_state.get("meds", ""))
    allergies = st.text_area("Allergies", value=st.session_state.get("allergies", ""))
    findings = st.text_area("Objective (Findings)", value=st.session_state.get("findings", ""))
    diagnosis = st.text_area("Assessment", value=st.session_state.get("diagnosis", ""))
    treatment = st.text_area("Plan", value=st.session_state.get("treatment", ""))

# --- PDF Upload ---
with st.expander("📄 Upload Referral or History (PDF)", expanded=False):
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

# --- Radiograph Comparison ---
with st.expander("🩻 Upload Radiographs (Optional)", expanded=False):
    old_xray = st.file_uploader("Previous Radiograph", type=["jpg", "jpeg", "png"], key="old_xray")
    new_xray = st.file_uploader("Current Radiograph", type=["jpg", "jpeg", "png"], key="new_xray")
    xray_summary = ""

    if old_xray and new_xray and st.button("🔍 Analyze with GPT-4 Vision"):
        images = [{"image": old_xray.getvalue(), "desc": "This is the earlier radiograph."},
                  {"image": new_xray.getvalue(), "desc": "This is the more recent radiograph."}]
        vision_inputs = []
        for img in images:
            b64 = base64.b64encode(img["image"]).decode("utf-8")
            vision_inputs.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}})
            vision_inputs.append({"type": "text", "text": img["desc"]})
        try:
            result = client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[{"role": "user", "content": vision_inputs}],
                max_tokens=500
            )
            xray_summary = result.choices[0].message.content
            st.markdown("### 🧠 GPT Vision Radiograph Summary")
            st.markdown(xray_summary)
        except Exception as e:
            st.error(f"Vision error: {e}")

# --- Chairside Assistant ---
with st.expander("🪥 Chairside Diagnostic Assistant"):
    odontogram = st.text_area("Odontogram Summary")
    perio = st.text_area("Periodontal Summary")
    if odontogram or perio:
        st.markdown("#### Combined Clinical Impression:")
        st.markdown(f"- Odontogram: {odontogram}\n- Perio: {perio}")

# --- Consent Generator ---
with st.expander("📑 Consent Generator"):
    procedure = st.text_input("Procedure")
    lang = st.selectbox("Language", ["English", "Spanish", "Russian", "Haitian Creole"])
    if st.button("Generate Consent"):
        consent = f"Consent for {procedure} ({lang})\n- Risks: pain, bleeding, failure\n- Alternatives discussed\n- Patient consented after all questions answered."
        st.text_area("Consent Output", value=consent, height=200)

# --- Compliance Auditor ---
with st.expander("⚖️ Compliance Auditor"):
    audit_text = st.text_area("Paste SOAP Note")
    if st.button("Run Compliance Check"):
        flags = []
        if "risks" not in audit_text.lower(): flags.append("Missing risk disclosure")
        if "alternative" not in audit_text.lower(): flags.append("Missing alternative discussion")
        if "consent" not in audit_text.lower(): flags.append("Missing consent confirmation")
        if flags:
            for flag in flags:
                st.error(f"⚠️ {flag}")
        else:
            st.success("✅ All legal/compliance phrases found.")

# --- De-ID Toggle ---
deid_enabled = st.checkbox("🛡 De-identify before GPT", value=True)

# --- Generate Final Note ---
if st.button("📝 Generate Full Note"):
    base_note = f"S: {history}\nO: Meds: {meds}\nAllergies: {allergies}\nFindings: {findings}\nA: {diagnosis}\nP: {treatment}"
    if parsed_text:
        base_note += f"\n\n[Scanned Doc]\n{parsed_text}"
    if xray_summary:
        base_note += f"\n\n[Radiograph Summary]\n{xray_summary}"

    
        if radiograph_summary:
            base_note += f"\n\n[Radiograph Findings]\n{radiograph_summary}"
        if pdf_text:
            base_note += f"\n\n[Referral Summary]\n{pdf_text}"
        if assistant_enabled:
            base_note += f"\n\n[Chairside Notes]\nPerio: {perio}\nOdontogram: {odontogram}"
        if procedure and consent_enabled:
            consent = f"Consent for {procedure} ({lang})\n- Risks: pain, bleeding, failure\n- Alternatives discussed\n- Patient consented after all questions were answered."
            base_note += f"\n\n[Consent]\n{consent}"

        base_note += "\n\n[Compliance Addendum]\nPatient was informed of all risks, given alternative options, and all questions were answered."


    if deid_enabled:
        base_note, replacements = deidentify(base_note)
        st.info("PHI removed before GPT")

    try:
        result = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "Format this as a formal SOAP note for dental charting."},
                      {"role": "user", "content": base_note}],
            max_tokens=800
        )
        output = result.choices[0].message.content
        if deid_enabled:
            output = reidentify(output, replacements)
        st.text_area("🧾 Final SOAP Note", value=output, height=400)
    except Exception as e:
        st.error(f"GPT Error: {e}")
