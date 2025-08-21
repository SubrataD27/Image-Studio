from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("GROQ_API_KEY not found. Did you set it in .env?")

# Initialize client
client = Groq(api_key=API_KEY)

# Send a prompt to the model
completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "Write a short poem about the sunrise."}
    ],
    temperature=0.7,
    max_completion_tokens=200,
)

# Print the output
print(completion.choices[0].message.content)
