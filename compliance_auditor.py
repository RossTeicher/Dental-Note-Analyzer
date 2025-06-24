
import openai

def audit_compliance(soap_text, treatment_plan):
    prompt = f"""
    You are a dental legal compliance and insurance auditor AI.

    Assess the following SOAP note and treatment plan for:
    - Missing legal phrases (e.g., no documentation of risks or consent)
    - Insurance red flags (e.g., CDT code mismatches, unsupported procedures)
    - Documentation requirements for certain procedures
    - Follow-up plan gaps
    - Suggest wording or actions to improve compliance

    SOAP NOTE:
    {soap_text}

    TREATMENT PLAN:
    {treatment_plan}

    Return a clear summary with ✅ compliant areas and 🚨 flagged issues. End with a ✔️ legal improvement checklist.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )

    return response.choices[0].message["content"]
