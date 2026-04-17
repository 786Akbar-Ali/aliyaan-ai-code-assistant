import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
print(f"API key loaded: {'Yes' if api_key else 'No'}")

if api_key:
    client = Groq(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": "Say 'API works!'"}],
            max_tokens=10
        )
        print("✅ API call successful:", response.choices[0].message.content)
    except Exception as e:
        print("❌ API call failed:", e)
else:
    print("❌ No API key found. Check .env file location and content.")