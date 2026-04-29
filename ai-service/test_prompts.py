import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def load_prompt(title, severity, start_time, end_time, affected_systems, description):
    with open("prompts/describe_prompt.txt", "r") as f:
        template = f.read()
    from datetime import datetime
    return template.format(
        title=title,
        severity=severity,
        start_time=start_time,
        end_time=end_time,
        affected_systems=affected_systems,
        description=description,
        generated_at=datetime.utcnow().isoformat()
    )

def call_groq(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "llama-3.3-70b-versatile",
        "temperature": 0.3,
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(GROQ_URL, headers=headers, json=body)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# 5 test inputs
test_cases = [
    {
        "title": "Database Connection Pool Exhausted",
        "severity": "HIGH",
        "start_time": "2026-04-21 14:00",
        "end_time": "2026-04-21 14:45",
        "affected_systems": "PostgreSQL, Order Service",
        "description": "All DB connections were exhausted causing order processing to fail."
    },
    {
        "title": "Payment Gateway Timeout",
        "severity": "CRITICAL",
        "start_time": "2026-04-20 09:15",
        "end_time": "2026-04-20 10:00",
        "affected_systems": "Payment Service, Checkout API",
        "description": "Payment gateway returned 504 errors for all transactions."
    },
    {
        "title": "CDN Cache Invalidation Failure",
        "severity": "MEDIUM",
        "start_time": "2026-04-19 16:00",
        "end_time": "2026-04-19 17:30",
        "affected_systems": "Frontend CDN",
        "description": "Stale assets served to users after a deployment."
    },
    {
        "title": "Redis Eviction Spike",
        "severity": "LOW",
        "start_time": "2026-04-18 11:00",
        "end_time": "2026-04-18 11:20",
        "affected_systems": "Redis Cache",
        "description": "Memory limit hit causing aggressive eviction of session data."
    },
    {
        "title": "API Rate Limit Breach",
        "severity": "MEDIUM",
        "start_time": "2026-04-17 13:00",
        "end_time": "2026-04-17 13:10",
        "affected_systems": "External API Gateway",
        "description": "Third-party API returned 429s due to misconfigured retry logic."
    }
]

for i, tc in enumerate(test_cases, 1):
    print(f"\n--- Test {i}: {tc['title']} ---")
    prompt = load_prompt(**tc)
    result = call_groq(prompt)
    try:
        parsed = json.loads(result)
        print(json.dumps(parsed, indent=2))
        print(" Valid JSON")
    except json.JSONDecodeError:
        print("INVALID JSON — raw output:")
        print(result)