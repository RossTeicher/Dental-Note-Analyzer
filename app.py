
import streamlit as st

st.title("🧠 BrightBite vToggles-Test")
st.info("✅ Toggle UI is Active - June 25 Fix")

# Define toggles early
fullstack_enabled = st.checkbox("⚙️ Enable Full-Stack Automation", value=True)
auto_legal_insert = st.checkbox("🛡 Auto-Complete Missing Legal Phrases", value=True)

# Example condition using toggles
if fullstack_enabled:
    st.success("✅ Full-Stack Automation is enabled.")

if auto_legal_insert:
    st.success("✅ Auto-Completion for Legal Phrases is enabled.")

# Placeholder for future logic
st.text_area("SOAP Note", "Enter note content here...")
