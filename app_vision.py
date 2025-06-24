
import streamlit as st
import openai
from PIL import Image

st.title("Dental Note Analyzer with GPT-4 Vision")

uploaded_images = st.file_uploader(
    "Upload today's radiographs (JPG/PNG only)",
    accept_multiple_files=True,
    type=["jpg", "jpeg", "png"]
)

radiograph_findings = []

if uploaded_images:
    for img_file in uploaded_images:
        image = Image.open(img_file)
        st.image(image, caption=f"Uploaded: {img_file.name}", use_column_width=True)

        # Vision Prompt
        prompt = """
        You are a dental radiologist AI. Analyze this dental radiograph and provide:
        1. Signs of decay, bone loss, infections, or abnormalities
        2. Tooth numbers involved (if visible)
        3. Signs of prior treatment (implants, crowns, root canals)
        4. Overall impression
        """

        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_file.getvalue().hex()}" }}
                ]}
            ],
            max_tokens=800
        )

        finding = response.choices[0].message["content"]
        st.markdown(f"**GPT-4 Vision Analysis for {img_file.name}:**")
        st.write(finding)
        radiograph_findings.append(finding)

# These findings would now be passed into the SOAP note generator in the full app.
