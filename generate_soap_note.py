
import openai

def generate_soap_note(patient_data, radiograph_findings):
    cdt_code_map = {
        "D0150": "Comprehensive oral evaluation - new or established patient",
        "D1110": "Prophylaxis - adult",
        "D2392": "Resin-based composite - two surfaces, posterior",
        "D2740": "Crown - porcelain/ceramic substrate",
        "D3310": "Endodontic therapy, anterior tooth (excluding final restoration)"
    }

    today_summary = ""
    # Dummy example for now
    completed_today = [
        {"code": "D0150", "tooth": ""},
        {"code": "D1110", "tooth": ""},
        {"code": "D2392", "tooth": "#30"},
        {"code": "D2740", "tooth": "#8"},
    ]

    for proc in completed_today:
        desc = cdt_code_map.get(proc["code"], "Unknown procedure")
        tooth = proc.get("tooth", "")
        today_summary += f"- {desc} ({proc['code']}) on {tooth if tooth else 'unspecified tooth'}\n"

    findings_summary = "\n".join(radiograph_findings)

    prompt = f"""
    Generate a legally formatted SOAP note based on the following:

    PATIENT DATA:
    {patient_data}

    TODAY'S VISIT:
    {today_summary}

    RADIOGRAPH FINDINGS:
    {findings_summary}

    Include subjective complaints, objective chart findings, assessment, and a treatment plan. Be precise, formal, and comprehensive.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message["content"]
