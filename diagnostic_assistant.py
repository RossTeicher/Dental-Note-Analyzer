
import openai

def generate_diagnostic_summary(chart_data, odo_data, perio_data, doc_data, radiograph_findings):
    prompt = f"""
    You are a chairside dental diagnostic assistant. Given the following patient data, generate a tooth-by-tooth diagnostic summary.

    1. Identify all relevant conditions (e.g., caries, bone loss, missing teeth, RCT failure, open margins).
    2. For each condition, specify the tooth number and supporting findings (from odontogram, perio, radiographs).
    3. Provide recommendations: monitoring, further imaging, or treatment (e.g., "Consider PA on #30").
    4. Be concise, precise, and legally appropriate.

    PATIENT CHART:
    {chart_data}

    ODONTOGRAM:
    {odo_data}

    PERIO CHART:
    {perio_data}

    CLINICAL NOTES:
    {doc_data}

    RADIOGRAPH FINDINGS:
    {radiograph_findings}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message["content"]
