from llm import call_llm
import json

def clean_response(response):
    response = response.replace("```json", "").replace("```", "").strip()
    return response

def generate_summary(data):
    prompt = f"""
    Based on this website content:

    {data['content']}

    Return ONLY JSON:
    {{
      "company_summary": "...",
      "industry": "...",
      "estimated_size": "...",
      "location": "...",
      "revenue_range": "..."
    }}
    """

    response = call_llm(prompt)

    if not response:
        return {
            "company_summary": "SaaS company offering digital products.",
            "industry": "SaaS",
            "estimated_size": "20-50 employees",
            "location": "US",
            "revenue_range": "$5M-$50M"
        }

    response = clean_response(response)

    try:
        parsed = json.loads(response)

        if isinstance(parsed.get("company_summary"), str):
            parsed["company_summary"] = parsed["company_summary"].replace("```json", "").replace("```", "").strip()

        return parsed

    except:
        return {
            "company_summary": response,
            "industry": "SaaS",
            "estimated_size": "20-50 employees",
            "location": "US",
            "revenue_range": "$5M-$50M"
        }