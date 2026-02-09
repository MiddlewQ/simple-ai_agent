import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise Exception("no api key")

client = genai.Client(api_key=api_key)

model = "gemini-2.5-flash"
prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

print(f"User prompt: {prompt}")

response = client.models.generate_content(model=model, contents=prompt)
print(response.text)
usage_stats = response.usage_metadata
print(f"User tokens: {usage_stats.prompt_token_count}")
print(f"Response token count: {usage_stats.total_token_count}")