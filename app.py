import streamlit as st
from synthesia_stub import generate_synthesia_script

st.title("🎥 Synthesia Patient Education Video Generator")

procedure = st.selectbox("Procedure", ["Implant", "Crown", "Root Canal", "Extraction", "Scaling & Root Planing"])
language = st.selectbox("Language", ["English", "Spanish", "Russian", "French", "Haitian Creole"])

if st.button("Generate Video Script"):
    with st.spinner("Creating patient-friendly script..."):
        script = generate_synthesia_script(procedure, language)
        st.success("✅ Script Generated!")
        st.text_area("Synthesia Video Script", script, height=300)

        st.markdown("### ▶️ Example Video (Placeholder)")
        st.video("https://cdn.synthesia.io/examples/website-demo.mp4")  # Placeholder link
