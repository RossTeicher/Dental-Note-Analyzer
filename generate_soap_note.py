
import openai

def generate_soap_note(patient_data, completed_today):
    cdt_code_map = {
        "D0150": "Comprehensive oral evaluation - new or established patient",
        "D1110": "Prophylaxis - adult",
        "D2392": "Resin-based composite - two surfaces, posterior",
        "D2740": "Crown - porcelain/ceramic substrate",
        "D3310": "Endodontic therapy, anterior tooth (excluding final restoration)"
    }

    today_summary = ""
    for proc in completed_today:
        desc = cdt_code_map.get(proc["code"], "Unknown procedure")
        tooth = proc.get("tooth", "")
        today_summary += f"- {desc} ({proc['code']}) on {tooth if tooth else 'unspecified tooth'}\n"

    prompt = f"""
    Generate a legally formatted SOAP note based on the following:

    PATIENT DATA:
    {patient_data}

    TODAY'S VISIT:
    {today_summary}

    Include subjective complaints, objective chart findings, assessment, and a treatment plan. Be precise, formal, and comprehensive.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message["content"]
