# Dental Note Analyzer

This Streamlit app allows you to generate AI-powered dental SOAP notes, diagnoses, treatment plans, and patient handouts from clinical data.

## Features
- Upload perio charts and radiographs
- Generate full clinical documentation with GPT-4o
- Extract and generate a PDF with only patient-facing content
- Designed for case acceptance and layman understanding

## Setup
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Add your OpenAI API key to `.streamlit/secrets.toml`:
   ```
   [general]
   OPENAI_API_KEY = "your-api-key-here"
   ```

3. Run the app:
   ```
   streamlit run app.py
   ```
