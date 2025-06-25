import streamlit as st

# Toggle states
fullstack_enabled = st.sidebar.checkbox("Enable Full Stack Automation")
deid_enabled = st.sidebar.checkbox("De-identify before GPT")

# Sample inputs
st.title("BrightBite - AI Dental Assistant")
st.subheader("SOAP Note Generator")

patient_name = st.text_input("Patient Name")
dob = st.text_input("Date of Birth")
history = st.text_area("Subjective History")
objective = st.text_area("Objective Findings")
assessment = st.text_area("Assessment")
plan = st.text_area("Planned Treatment")

# Run automation
if st.button("▶️ Run Full Stack Automation"):
    note = f"S: {history}\nO: {objective}\nA: {assessment}\nP: {plan}"
    if deid_enabled:
        note = note.replace(patient_name, "[REDACTED]").replace(dob, "[REDACTED DOB]")
    if fullstack_enabled:
        note += "\n\n[Automated Legal Insert] All patient questions were answered. Patient was offered the option to do nothing."
    st.success("Generated SOAP Note:")
    st.code(note, language="markdown")
