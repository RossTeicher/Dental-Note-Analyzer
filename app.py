import streamlit as st
from openai import OpenAI
import os
from PIL import Image
import pytesseract
import tempfile
from pdf2image import convert_from_path
from openai import OpenAI, OpenAIError
import base64
import re
from fpdf import FPDF

oai_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=oai_key)

st.title("🦷 AI Dental Analyzer - Phase 4: Expanded Data Integration")

st.markdown("Upload today's data and prior information for a deep analysis.")

procedure_codes = st.text_area("Enter Procedure Codes", "D1110, D4341")
perio_chart_file = st.file_uploader("Upload Perio Chart", type=["png", "jpg", "jpeg", "pdf"])
radiograph_file = st.file_uploader("Upload Today's Radiograph", type=["png", "jpg", "jpeg"])
previous_radiograph_file = st.file_uploader("Upload Previous Radiograph", type=["png", "jpg", "jpeg"])
intraoral_images = st.file_uploader("Upload Intraoral Photos", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
docs = st.file_uploader("Upload Additional Documents", type=["pdf", "txt"], accept_multiple_files=True)
previous_notes = st.file_uploader("Upload Previous SOAP Notes", type=["pdf", "txt"], accept_multiple_files=True)

def extract_text(uploaded_file):
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
            try:
                if uploaded_file.type == "application/pdf":
                    images = convert_from_path(tmp_path)
                    return "\n".join([pytesseract.image_to_string(img) for img in images])
                else:
                    img = Image.open(tmp_path)
                    return pytesseract.image_to_string(img)
            except Exception as e:
                return f"OCR Error: {e}"
    return ""

def aggregate_text(file_list):
    text = ""
    for f in file_list:
        extracted = extract_text(f)
        if extracted:
            text += f"\n---\n{extracted}"
    return text

def get_image_data(file):
    if file:
        encoded = base64.b64encode(file.read()).decode("utf-8")
        return {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded}"}}
    return None

generate = st.button("Generate Comprehensive AI Note")

if generate and procedure_codes and perio_chart_file:
    with st.spinner("Analyzing all uploaded content..."):
        try:
            perio_text = extract_text(perio_chart_file)
            rad_today = get_image_data(radiograph_file)
            rad_prev = get_image_data(previous_radiograph_file)
            intraoral_summaries = [get_image_data(img) for img in intraoral_images] if intraoral_images else []
            doc_text = aggregate_text(docs) if docs else ""
            old_notes = aggregate_text(previous_notes) if previous_notes else ""

            messages = [
                {"role": "system", "content": "You are a senior dental AI analyst reviewing complete clinical context."},
                {"role": "user", "content": f"Today's Procedure Codes: {procedure_codes}"},
                {"role": "user", "content": f"Periodontal Chart: {perio_text}"},
                {"role": "user", "content": f"Additional Documents: {doc_text}"},
                {"role": "user", "content": f"Previous Notes: {old_notes}"},
                {"role": "user", "content": "If intraoral and radiograph images are present, analyze them for findings. Compare today's radiograph with any prior radiograph and note any progression, regression, or unchanged findings."},
                {"role": "user", "content": "Summarize: (1) A SOAP note (2) Diagnosis (3) Differential (4) Treatment options including do-nothing (5) Progress tracking from previous notes (6) Patient education worksheet (7) Risk warning sheet"}
            ]

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )

            output = response.choices[0].message.content

            st.subheader("📋 Full AI Note Output")
            st.text_area("Output", output, height=500)

        except Exception as e:
            st.error(f"Error: {e}")
