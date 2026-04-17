import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
print(f"API key loaded: {'Yes' if api_key else 'No'}")
if api_key:
    print(f"First 5 chars: {api_key[:5]}...")
else:
    print("❌ No API key found. Check .env file.")

if api_key:
    client = Groq(api_key=api_key)
    # Test with a known working model
    try:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",  # safe model
            messages=[{"role": "user", "content": "Say OK"}],
            max_tokens=5
        )
        print("✅ API works:", response.choices[0].message.content)
    except Exception as e:
        print("❌ API error:", e)