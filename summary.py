from llm import call_llm
import json
import re


def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)
    return None


def generate_summary(data, company_name="Company"):
    content = data.get("content", "")[:500]

    prompt = f"""
    Return ONLY valid JSON.
    No markdown.
    No explanation.
    No extra text.

    Company: {company_name}
    Website content:
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

    if not response:
        return {
            "company_summary": "Unable to analyze company",
            "industry": "Unknown",
            "estimated_size": "Unknown",
            "location": "Unknown",
            "revenue_range": "Unknown",
            "outreach_email": f"Hi {company_name} team, would love to connect."
        }

    try:
        return json.loads(response)

    except Exception:
        extracted = extract_json(response)

        if extracted:
            try:
                return json.loads(extracted)
            except Exception:
                pass

    return {
        "company_summary": data.get("meta_description", "Unable to analyze company"),
        "industry": "Unknown",
        "estimated_size": "Unknown",
        "location": "Unknown",
        "revenue_range": "Unknown",
        "outreach_email": f"Hi {company_name} team, would love to connect."
    }
