
import openai

def generate_soap_note(patient_data, radiograph_findings, perio_data=None, odontogram_data=None, documents=None):
    today_summary = ""
    completed_today = patient_data.get("procedures", [])
    cdt_code_map = {
        "D0150": "Comprehensive oral evaluation",
        "D1110": "Prophylaxis - adult",
        "D2392": "Resin-based composite - two surfaces, posterior",
        "D2740": "Crown - porcelain/ceramic substrate",
        "D3310": "Endodontic therapy, anterior tooth"
    }

    for proc in completed_today:
        code = proc.get("Code", "")
        desc = cdt_code_map.get(code, "Unknown procedure")
        tooth = proc.get("Tooth", "")
        today_summary += f"- {desc} ({code}) on {tooth if tooth else 'unspecified'}\n"

    findings_summary = "\n".join(radiograph_findings)
    doc_summary = "\n".join(documents) if documents else ""

    prompt = f"""
    You are a clinical documentation assistant. Based on the following inputs, write a legally formatted SOAP note.

    PATIENT DATA:
    {patient_data}

    TODAY'S VISIT:
    {today_summary}

    RADIOGRAPH FINDINGS:
    {findings_summary}

    PERIO CHART:
    {perio_data}

    ODONTOGRAM:
    {odontogram_data}

    EXTERNAL DOCUMENTS:
    {doc_summary}

    Format with Subjective, Objective, Assessment, and Plan. Summarize today's treatment, prior history, radiographic and periodontal findings, odontogram status, and referral documents.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message["content"]
