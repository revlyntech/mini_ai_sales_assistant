import os
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def call_llm(prompt, retries=3):
    for attempt in range(retries):
        try:
            print("Trying OpenRouter free router...")

            response = client.chat.completions.create(
                model="stepfun-ai/step-3.5-flash",
                messages=[
                    {"role": "user", "content": prompt}
                ]
                timeout=20
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"LLM Error attempt {attempt+1}: {e}")
            time.sleep(3)

    return "Unable to generate response currently."
