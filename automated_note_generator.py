
import os
from openai import OpenAI
from datetime import date
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

# Set your OpenAI API key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

procedure_codes = "D1110, D4341"
perio_chart_path = "perio_chart.pdf"
radiograph_path = "radiograph.jpg"

def extract_text_from_file(filepath):
    if filepath.endswith(".pdf"):
        images = convert_from_path(filepath)
        return "\n".join([pytesseract.image_to_string(img) for img in images])
    else:
        image = Image.open(filepath)
        return pytesseract.image_to_string(image)

def extract_radiograph_summary(filepath):
    return "Radiograph uploaded but analysis not yet implemented." if os.path.exists(filepath) else "No radiograph uploaded."

def generate_note():
    perio_text = extract_text_from_file(perio_chart_path)
    radiograph_summary = extract_radiograph_summary(radiograph_path)

    messages = [
        {"role": "system", "content": "You are a dental assistant helping to generate SOAP notes."},
        {"role": "user", "content": f"Here are the procedure codes: {procedure_codes}"},
        {"role": "user", "content": f"Here is the perio chart data: {perio_text}"},
        {"role": "user", "content": f"Radiograph summary: {radiograph_summary}"},
        {"role": "user", "content": "Based on this information, generate a periodontal diagnosis, list any red flags or possible conditions, and write a complete clinical note."}
    ]

    response = client.chat.completions.create(model="gpt-4-turbo", messages=messages)
    note = response.choices[0].message.content
    with open(f"note_{date.today()}.txt", "w") as f:
        f.write(note)
    print("Note generated and saved.")

if __name__ == "__main__":
    generate_note()
