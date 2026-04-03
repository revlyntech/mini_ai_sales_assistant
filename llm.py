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
            model="openrouter/auto",
            messages=[
                {"role": "user", "content": prompt}
            ],
            timeout=40
        )

        content = response.choices[0].message.content
        print("✅ OPENROUTER RESPONSE:", content[:300])
        return content

    except Exception as e:
        print("❌ OPENROUTER REAL ERROR:", str(e))
        return None
