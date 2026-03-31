from llm import call_llm

def generate_email(company, summary):
    prompt = f"""
    Write a short personalized cold email.

    Company: {company}
    About them: {summary}

    Sender Name: Krishnanshu
    Sender company: Revops Central
    Sender Role: Sales

    Rules:
    - Keep it under 120 words
    - Be natural and human
    - Avoid generic phrases

    Return only the email.
    """

    return call_llm(prompt)