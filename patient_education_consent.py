
import openai

def generate_patient_consent_package(chart_data, treatment_plan, language="English"):
    prompt = f"""
    You are a dental AI assistant tasked with creating a patient-facing consent and education packet.

    Use the following inputs:
    - PATIENT CHART: {chart_data}
    - TREATMENT PLAN: {treatment_plan}
    - LANGUAGE: {language}

    Your output should include:

    1. CONSENT FORM TEXT:
    A short, clear statement for the patient to read and sign. Include general risks and reference the treatment. Also include: "All patient questions were answered. The patient was also given the option of doing nothing."

    2. SCARY NOTE (layman's terms):
    Write a brief but serious summary of what could happen if the patient *does not* do the treatment. Avoid jargon.

    3. PATIENT EDUCATION:
    Explain in simple terms why this treatment is recommended. Reassure the patient, explain benefits, and what to expect.

    4. AI VIDEO DESCRIPTION:
    Write a short script that could be used for an AI-generated video that explains the procedure.

    Return all 4 parts in the selected language.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=1200
    )

    sections = response.choices[0].message["content"].split("\n\n")
    consent = next((s for s in sections if "CONSENT FORM" in s), "")
    scary = next((s for s in sections if "SCARY NOTE" in s), "")
    edu = next((s for s in sections if "PATIENT EDUCATION" in s), "")
    video = next((s for s in sections if "AI VIDEO DESCRIPTION" in s), "")

    return consent, scary, edu, video
