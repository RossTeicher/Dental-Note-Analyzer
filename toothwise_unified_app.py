st.set_page_config(page_title="ToothWise – AI Dental Assistant", page_icon="🧠")

import streamlit as st
from PIL import Image
import base64
import os

# Load logo
if "toothwise_logo.png" in os.listdir():
    logo = Image.open("toothwise_logo.png")
    st.image(logo, width=160)

st.title("ToothWise")
st.subheader("AI That Talks Smart. So You Don’t Have To.")

# Tabbed interface
tab = st.sidebar.radio("Navigate", ["Home", "App", "Demo Packet"])

if tab == "Home":
    st.markdown("""
### 🦷 Meet ToothWise

ToothWise is your AI-powered dental assistant, automating:
- 📝 SOAP Notes
- 📷 Radiograph Interpretation
- 📊 Treatment Plan Validation
- 🦷 Periodontal & Odontogram Integration
- 📑 Legal & Insurance Audit Trails
- 🌍 Multilingual Patient Education

Click the sidebar to explore the full app or view a sample treatment packet!
""")
elif tab == "App":
    from app import run_toothwise_app
    run_toothwise_app()
elif tab == "Demo Packet":
    if "Treatment_Options_And_Risks.pdf" in os.listdir():
        with open("Treatment_Options_And_Risks.pdf", "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    else:
        st.warning("Demo packet not found.")
