import os
import time
import logging
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.ERROR)

class GroqClient:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key)

    def generate_response(self, prompt):
        max_retries = 3

        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )

                return response.choices[0].message.content

            except Exception as e:
                logging.error(f"Attempt {attempt + 1} failed: {str(e)}")

                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # ✅ exponential backoff

        return "AI service is temporarily unavailable. Please try again later."