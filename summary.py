import json
import re
from llm import call_llm


def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else None


def generate_summary(data, company_name="Company"):
    content = data.get("content", "")[:500]

    prompt = f"""
    Return ONLY valid JSON.
    No markdown.
    No extra text.

    Company: {company_name}
    Website:
    {content}

    {{
      "company_summary": "...",
      "industry": "...",
      "estimated_size": "...",
      "location": "...",
      "revenue_range": "...",
      "outreach_email": "..."
    }}
    """

    response = call_llm(prompt)

    if response:
        extracted = extract_json(response) or response
        try:
            return json.loads(extracted)
        except:
            pass

    return {
        "company_summary": data.get("meta_description", "Unable to analyze"),
        "industry": "Unknown",
        "estimated_size": "Unknown",
        "location": "Unknown",
        "revenue_range": "Unknown",
        "outreach_email": f"Hi {company_name} team, would love to connect."
    }
