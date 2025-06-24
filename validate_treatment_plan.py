
import openai

def validate_treatment_plan(chart_data, treatment_plan, odo_data=None, perio_data=None, doc_data=None):
    prompt = f"""
    You are a dental AI assistant. Using the following data, validate the proposed treatment plan. Identify:
    - Missing procedures based on patient condition
    - Over-treatment or redundancy
    - Incorrect sequencing
    - Inconsistencies with radiographs, perio chart, or odontogram

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

    Provide a detailed validation summary with:
    ✅ Confirmed codes
    ⚠️ Potential issues
    💡 Suggestions for improvement
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message["content"]
