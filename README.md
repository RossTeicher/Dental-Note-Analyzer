# 🦷 AI-Powered Dental Note Generator

A Streamlit web app that helps dentists generate clinical notes using GPT-4 and simulated radiographic analysis. Includes example patients, automatic PDF export, and optional mock image interpretation.

## Features
- SOAP or narrative note generation
- Simulated radiograph interpretation
- PDF export for EHR or manual upload
- User-friendly UI for non-technical users

## Quick Start

1. Clone the repo or upload to GitHub.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the app locally:
   ```
   streamlit run app.py
   ```

## Deploy to Streamlit Cloud
1. Push to a GitHub repo
2. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Link your repo and deploy
4. Set `OPENAI_API_KEY` as a secret in the settings

## License
MIT
