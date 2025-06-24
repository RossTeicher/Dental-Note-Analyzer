
import openai

def validate_treatment_plan(chart_data, treatment_plan, odo_data=None, perio_data=None, doc_data=None):
    prompt = f"""
    You are a dental AI assistant. Using the following data, validate the proposed treatment plan for clinical, logical, and legal adequacy. Specifically:

    1. Verify whether the planned procedures match the clinical findings.
    2. Identify any missing, excessive, or improperly sequenced procedures.
    3. For each treatment option, list the advantages and disadvantages clearly.
    4. Conclude with the legal language: "All patient questions were answered. The patient was also given the option of doing nothing."

    PATIENT CHART:
    {chart_data}

    ODONTOGRAM:
    {odo_data}

    PERIO CHART:
    {perio_data}

    DOCUMENTS:
    {doc_data}

    PROPOSED TREATMENT PLAN:
    {treatment_plan}

    Return a detailed, legally defensible validation summary in plain English.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message["content"]
