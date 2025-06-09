
# 🦷 AI Dental Note Generator

This is a Streamlit-based application that uses OpenAI's GPT-4-turbo model to generate periodontal diagnoses and clinical notes based on:
- CDT procedure codes
- Uploaded perio charts (PDF or image)
- (Optionally) radiographs

---

## 🚀 Features

- Upload and analyze perio charts using OCR (Tesseract)
- Accepts CDT procedure codes as input
- Uses GPT-4-turbo to generate structured clinical documentation
- Runs entirely in your browser via Streamlit Cloud

---

## 📦 Files Included

- `app.py` — Main application logic (Streamlit + OpenAI)
- `requirements.txt` — Python packages to install
- `packages.txt` — System packages for Tesseract + Poppler
- `README.md` — This documentation

---

## ☁️ Streamlit Cloud Setup Instructions

1. **Upload the files to a GitHub repository**
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click **“New App”**, and select your GitHub repo
4. Streamlit Cloud will automatically install:
   - `tesseract-ocr` (from `packages.txt`)
   - Python packages (from `requirements.txt`)

5. **Set your OpenAI API Key** under app settings:
   - Click “⋮” > “Edit Secrets”
   - Paste:
     ```
     OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxx"
     ```

---

## 🛠️ Troubleshooting

- If the app crashes on load, ensure:
  - `tesseract-ocr` and `poppler-utils` are present in `packages.txt`
  - Your API key is active and has quota
- If the app fails with OCR errors, make sure your uploaded image/PDF is legible and clean

---

Built with ❤️ for smarter dental documentation.
