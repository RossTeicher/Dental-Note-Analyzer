
import streamlit as st

# Page config
st.set_page_config(page_title="BrightBite Dental Assistant", layout="wide")

# App title and logo
st.title("🧠🦷 BrightBite: AI Dental Assistant")
st.markdown("Welcome to the full-stack demo. Upload your files and click below to begin.")

# Toggles
st.sidebar.header("Modules")
deidentify_enabled = st.sidebar.checkbox("🔒 De-identify before GPT", value=True)
fullstack_enabled = st.sidebar.checkbox("⚙️ Full Stack Automation", value=True)
include_voice = st.sidebar.checkbox("🎤 Voice Dictation", value=False)

# Upload section
st.subheader("Upload Patient Files")
xray_files = st.file_uploader("Upload Radiographs", type=["jpg", "png"], accept_multiple_files=True)
pdf_file = st.file_uploader("Upload PDF Documents", type=["pdf"])
notes = st.text_area("Optional: Enter Observations or Findings")

# Automation trigger
if st.button("▶️ Run Full Stack Automation"):
    st.success("Processing all selected modules... (placeholder logic)")
    if fullstack_enabled:
        st.info("Running radiograph analysis, PDF parsing, risk stratification, and note generation.")
    if deidentify_enabled:
        st.info("De-identifying patient data before processing.")
    if include_voice:
        st.info("Voice dictation module enabled (not yet implemented).")

# Safety fallback
st.caption("If nothing appears above, ensure all dependencies are installed and try refreshing.")

