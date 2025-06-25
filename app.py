
import streamlit as st
from openai import OpenAI
from PIL import Image
import fitz  # PyMuPDF
import os
import base64


def deidentify(text):
    """Replace PHI with placeholders and track what to restore later."""
    replacements = {}
    # Very basic example; real use would use regex, NLP, or spaCy
    if "John Smith" in text:
        replacements["Patient A"] = "John Smith"
        text = text.replace("John Smith", "Patient A")
    if "01/01/1980" in text:
        replacements["[DOB]"] = "01/01/1980"
        text = text.replace("01/01/1980", "[DOB]")
    return text, replacements

def reidentify(text, replacements):
    """Restore real PHI after GPT processing."""
    for fake, real in replacements.items():
        text = text.replace(fake, real)
    return text


st.set_page_config(page_title="BrightBite - Dental Note Analyzer", layout="wide")
st.title("🧠🦷 BrightBite - Dental Note Analyzer")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

tabs = st.tabs([
    "SOAP Note Generator", "Radiograph Analyzer (GPT-4 Vision)",
    "PDF Parser", "Treatment Plan Validator",
    "Consent Generator", "Compliance Auditor"
])

with tabs[0]:
    st.header("📋 SOAP Note Generator")
    name = st.text_input("Patient Name", key="soap_name")
    subj = st.text_area("Subjective (Chief Complaint, History)", key="soap_subj")
    obj = st.text_area("Objective (Findings, Meds, Allergies)", key="soap_obj")
    assess = st.text_area("Assessment", key="soap_assess")
    plan = st.text_area("Plan", key="soap_plan")
    
    deid_enabled = st.checkbox("Auto-Deidentify PHI Before GPT", key="deid_toggle")
    if st.button("Generate SOAP Note", key="soap_button"):
        note = f"""S: {subj}
O: {obj}
A: {assess}
P: {plan}"""
        if deid_enabled:
            deid_note, replacements = deidentify(note)
            # Here you would call GPT on deid_note if needed
            note = reidentify(deid_note, replacements)
        st.text_area("Generated SOAP Note", value=note, height=300, key="soap_result")

        soap = f"""S: {subj}
O: {obj}
A: {assess}
P: {plan}"""
        st.text_area("Generated SOAP Note", value=soap, height=300, key="soap_result")

with tabs[1]:
    st.header("🩻 Radiograph Analyzer (GPT-4 Vision)")
    col1, col2 = st.columns(2)
    with col1:
        old_xray = st.file_uploader("Upload Previous Radiograph", type=["jpg", "jpeg", "png"], key="old_xray")
    with col2:
        new_xray = st.file_uploader("Upload Current Radiograph", type=["jpg", "jpeg", "png"], key="new_xray")

    if old_xray and new_xray:
        st.image(Image.open(old_xray), caption="Previous Radiograph", use_column_width=True)
        st.image(Image.open(new_xray), caption="Current Radiograph", use_column_width=True)

        if st.button("Analyze Changes with GPT-4 Vision", key="analyze_xray"):
            images = [
                {"image": old_xray.getvalue(), "desc": "This is the earlier radiograph."},
                {"image": new_xray.getvalue(), "desc": "This is the more recent radiograph."}
            ]
            messages = [
                {"role": "system", "content": "You are a dental radiologist. Compare the two images for any radiographic changes."},
                {"role": "user", "content": "Please compare these two dental radiographs and describe any changes, bone loss, or pathologies."}
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
                st.markdown("### 🧠 GPT-4 Vision Radiograph Comparison Result")
                st.markdown(result)
            except Exception as e:
                st.error(f"Error analyzing with GPT-4 Vision: {e}")

with tabs[2]:
    st.header("📄 PDF Parser")
    uploaded_pdf = st.file_uploader("Upload PDF Document", type=["pdf"], key="pdf_upload")
    if uploaded_pdf:
        pdf_path = f"temp_{uploaded_pdf.name}"
        with open(pdf_path, "wb") as f:
            f.write(uploaded_pdf.read())
        doc = fitz.open(pdf_path)
        extracted_text = ""
        for page in doc:
            extracted_text += page.get_text()
        st.text_area("Extracted Text", value=extracted_text, height=300, key="pdf_output")
        os.remove(pdf_path)

with tabs[3]:
    st.header("🛠️ Treatment Plan Validator")
    completed = st.text_area("Completed Procedures", key="completed_procs")
    planned = st.text_area("Planned Treatment", key="planned_tx")
    if st.button("Validate Plan", key="validate_plan_btn"):
        if "extraction" in planned.lower() and "crown" in completed.lower():
            st.warning("⚠️ Consider verifying viability of crowned teeth before extraction.")
        else:
            st.success("✅ No conflicts detected between planned and completed procedures.")

with tabs[4]:
    st.header("📑 Consent Generator")
    procedure = st.text_input("Procedure", key="consent_proc")
    language = st.selectbox("Language", ["English", "Spanish", "Russian", "Haitian Creole"], key="consent_lang")
    if st.button("Generate Consent", key="gen_consent_btn"):
        consent = f"""
Consent for {procedure} ({language})
- Risks: infection, discomfort, failure.
- Alternatives: doing nothing, other treatment options.
- All patient questions answered. Patient consents to proceed."""
        st.text_area("Generated Consent Form", value=consent, height=250, key="consent_output")

with tabs[5]:
    st.header("⚖️ Compliance Auditor")
    audit_note = st.text_area("Paste SOAP Note for Audit", key="audit_note")
    if st.button("Audit Note", key="audit_btn"):
        issues = []
        if "risks" not in audit_note.lower(): issues.append("Missing risk disclosure.")
        if "alternative" not in audit_note.lower(): issues.append("Missing treatment alternatives.")
        if "consent" not in audit_note.lower(): issues.append("Missing patient consent confirmation.")
        if issues:
            for issue in issues:
                st.error(f"⚠️ {issue}")
        else:
            st.success("✅ All legal elements present in note.")
