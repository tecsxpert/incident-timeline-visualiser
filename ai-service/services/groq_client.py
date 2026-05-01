import os
import time
import logging
from groq import Groq

logger = logging.getLogger(__name__)

def call_groq(prompt: str, retries: int = 3) -> str | None:  
    client = Groq(api_key=os.getenv("GROQ_API_KEY"), timeout=15)  # ↓ CHANGED: added timeout=15

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=800  # ↓ CHANGED: reduced from 1000 to keep under 2s
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Groq API error on attempt {attempt + 1}: {e}")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
    return None