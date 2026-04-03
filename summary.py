from llm import call_llm
import json


def clean_response(response):
    if not response:
        return ""
    return response.replace("```json", "").replace("```", "").strip()


def generate_summary(data, company_name="Company"):
    content = data.get("content", "")[:500]

    prompt = f"""
    You are a senior B2B SDR assistant.

    Analyze this website content and return ONLY valid JSON.

    Company: {company_name}
    Website content:
    {content}

    JSON format:
    {{
      "company_summary": "...",
      "industry": "...",
      "estimated_size": "...",
      "location": "...",
      "revenue_range": "...",
      "outreach_email": "..."
    }}

    Rules:
    - summary under 50 words
    - mention one business capability in email
    - include clear CTA
    - email under 80 words
    - return plain JSON only
    """

    response = call_llm(prompt)

    fallback = {
        "company_summary": "SaaS company offering digital products.",
        "industry": "SaaS",
        "estimated_size": "20-50 employees",
        "location": "United States",
        "revenue_range": "$5M-$50M",
        "outreach_email": (
            f"Hi {company_name} team,\n\n"
            f"I noticed your strong platform capabilities and focus on business efficiency. "
            f"RevOps Central helps SaaS teams improve lead qualification and GTM workflows.\n\n"
            f"Would you be open to a quick 15-minute conversation next week?"
        )
    }

    if not response:
        return fallback

    response = clean_response(response)

    try:
        parsed = json.loads(response)

        for key, value in fallback.items():
            if key not in parsed or not parsed[key]:
                parsed[key] = value

        return parsed

    except Exception:
        return fallback
