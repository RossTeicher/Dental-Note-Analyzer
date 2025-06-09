# AI Dental Note Generator (GPT-4 Vision Enabled)

This app uses GPT-4 Vision to generate dental SOAP notes, diagnoses, and treatment plans based on:
- Procedure codes
- Periodontal chart (PDF or image)
- Radiographs (analyzed via GPT-4 Vision)

## Setup
1. Upload to Streamlit Cloud or run locally
2. Set your `OPENAI_API_KEY` in `.streamlit/secrets.toml` or environment variables
3. Install requirements and system packages listed in `packages.txt`

## Run
```bash
streamlit run app.py
```