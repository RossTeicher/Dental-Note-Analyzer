
import streamlit as st
from PIL import Image

# Set page config
st.set_page_config(page_title="SmartMouth", page_icon="🧠", layout="centered")

# Load logo
logo = Image.open("smartmouth_logo.png")
st.image(logo, width=180)

st.title("AI That Talks Smart. So You Don’t Have To.")
st.subheader("The first AI-powered dental assistant that automates notes, audits plans, interprets X-rays, and educates patients.")

st.markdown("### 🚀 What SmartMouth Does")
features = [
    "📝 **SOAP Note Generator** – Legal-grade notes in seconds",
    "📋 **Treatment Plan Auditor** – Flags missing info, code mismatches",
    "🧠 **Chairside Diagnostic Assistant** – GPT-powered differential builder",
    "🦷 **Radiograph Reviewer** – Dental radiologist-style AI comparisons",
    "🗣️ **Smart Consent Generator** – Risk-based, multilingual, and printable",
    "🛡️ **Compliance Monitor** – Legal and insurance audit in real time"
]
for f in features:
    st.markdown(f)

st.markdown("### 📽️ Watch It In Action")
st.info("🛠️ Demo video placeholder — final video coming soon!")

st.markdown("### 📄 Download Demo Packet")
with open("Treatment_Options_And_Risks.pdf", "rb") as f:
    st.download_button("📥 Download PDF Example", data=f, file_name="SmartMouth_Demo.pdf", mime="application/pdf")

st.markdown("### 📬 Join Our Beta List")
email = st.text_input("Enter your email to get early access:")
if st.button("💌 Submit"):
    with open("leads.csv", "a") as f:
        f.write(email + "\n")
    st.success("You're on the list! We'll be in touch soon.")

st.markdown("### 👨‍⚕️ Meet the Founder")
st.markdown("""
**Ross Teicher, DDS, FAAIP, FAGD, FICOI**

“Dentists should focus on patient care — not paperwork. That’s why I built SmartMouth.”

*Implants. Sedation. TMJ. General Dentistry.* Now fully AI-powered.
""")

st.markdown("### 🧪 Ready to Try It?")
st.page_link("app.py", label="🦷 Launch the SmartMouth Demo", icon="🧠")
