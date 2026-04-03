import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


def call_llm(prompt):
    try:
        response = client.chat.completions.create(
            model="stepfun-ai/step-3.5-flash",
            messages=[
                {"role": "user", "content": prompt}
            ],
            timeout=20
        )
        return response.choices[0].message.content

    except Exception as e:
        print("LLM Error:", e)
        return None
