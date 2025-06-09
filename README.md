
# 🦷 AI Dental Note Generator

This is a Streamlit app that uses OpenAI's GPT-4-turbo to generate periodontal diagnoses and clinical notes based on uploaded procedure codes, perio charts, and (optionally) radiographs.

## 🚀 Features
- Upload procedure codes and perio chart files (image or PDF)
- Optical Character Recognition (OCR) of perio chart using Tesseract
- Generates periodontal diagnosis and SOAP-style clinical note with GPT
- Designed for daily use by dental professionals

## 🧱 Project Structure

```
/dental-note-analyzer/
├── app.py               # Main Streamlit app
├── requirements.txt     # Python dependencies
└── packages.txt         # System-level packages for Streamlit Cloud
```

## 🛠️ Installation (Streamlit Cloud)

### 1. Required Files
Make sure your GitHub repo includes:
- `app.py`
- `requirements.txt`
- `packages.txt`

### 2. packages.txt (for Streamlit Cloud)
Streamlit Cloud requires system-level packages to be listed in `packages.txt`:
```
tesseract-ocr
poppler-utils
```

These enable:
- OCR via `pytesseract` (needs `tesseract-ocr`)
- PDF-to-image conversion via `pdf2image` (needs `poppler-utils`)

### 3. requirements.txt
Make sure this includes:
```
streamlit
openai
pillow
pytesseract
pdf2image
```

### 4. Deploying on Streamlit Cloud
- Push your repo to GitHub
- Go to [Streamlit Cloud](https://streamlit.io/cloud)
- Create a new app and link it to your GitHub repo
- Streamlit Cloud will auto-install the listed packages and run your app

## 🧪 Usage
1. Run the app
2. Enter procedure codes (e.g., `D1110, D4341`)
3. Upload a perio chart file (image or PDF)
4. (Optional) Upload a radiograph image
5. Click **Generate Note** — the app will:
   - OCR the perio chart
   - Use GPT to analyze all data
   - Display a complete note with suggested diagnosis

## 🧰 Troubleshooting

If OCR isn't working, make sure the app has installed:
- `tesseract-ocr` (via `packages.txt`)
- `poppler-utils` (for PDF support)

If you encounter any OpenAI errors:
- Confirm your `OPENAI_API_KEY` is set using Streamlit Secrets
- Example format:
```toml
# .streamlit/secrets.toml
OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxx"
```

---

Built with ❤️ to make dental documentation smarter.
