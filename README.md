# Incident Timeline Visualiser

Python microservice that provides AI-powered analysis for the Incident Timeline Visualiser using Groq (LLaMA-3.3-70b).

---

## Tech Stack

| Technology | Version |
|---|---|
| Python | 3.11 |
| Flask | 3.1.3 |
| Groq API | 1.1.1 |
| Redis | 5.0.4 |
| flask-limiter | 4.1.1 |

---

## Folder Structure

```
ai-service/
├── routes/
│   ├── describe.py          # POST /ai/describe
│   ├── recommend.py         # POST /ai/recommend
│   ├── generate_report.py   # POST /ai/generate-report
│   └── health.py            # GET /health
├── services/
│   ├── groq_client.py       # Groq API calls with retry
│   ├── ai_cache.py          # Redis cache logic
│   └── cache_client.py      # Redis connection
├── prompts/
│   ├── describe_prompt.txt
│   ├── recommend_prompt.txt
│   └── generate_report_prompt.txt
├── app.py
├── Dockerfile
├── requirements.txt
└── .env
```

---

## Prerequisites

- Python 3.11
- Redis 7 (running via Docker or locally)
- Groq API key — free at [console.groq.com](https://console.groq.com)

---

## Setup

**1. Clone the repo and go to the ai-service folder:**
```bash
cd ai-service
```

**2. Create a virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Create your `.env` file:**
```bash
cp .env.example .env
```
Then fill in your values (see Environment Variables below).

**5. Run the service:**
```bash
python app.py
```
Service runs on `http://localhost:5000`

---

## Environment Variables

| Variable | Description | Example |
|---|---|---|
| `GROQ_API_KEY` | Your Groq API key | `gsk_xxx...` |
| `REDIS_HOST` | Redis host | `localhost` |
| `REDIS_PORT` | Redis port | `6379` |

`.env.example`:
```
GROQ_API_KEY=your_groq_api_key_here
REDIS_HOST=localhost
REDIS_PORT=6379
```

---

## Running with Docker

```bash
docker build -t ai-service .
docker run -p 5000:5000 --env-file .env ai-service
```

Or run the full stack via Docker Compose from the root folder:
```bash
docker-compose up --build
```

---

## API Reference

### GET /health
Check service status, uptime, and average response time.

**Request:**
```
GET http://localhost:5000/health
```

**Response:**
```json
{
  "status": "ok",
  "model": "llama-3.3-70b-versatile",
  "uptime_seconds": 120,
  "avg_response_time_ms": 1850.5,
  "redis": "connected"
}
```

---

### POST /ai/describe
Generate a structured AI description of an incident.

**Request:**
```json
{
  "title": "Database Connection Pool Exhausted",
  "severity": "HIGH",
  "description": "All DB connections were exhausted causing order processing to fail.",
  "affected_systems": "PostgreSQL, Order Service",
  "start_time": "2026-04-21 14:00",
  "end_time": "2026-04-21 14:45"
}
```

**Response:**
```json
{
  "summary": "A connection pool exhaustion event occurred on the PostgreSQL database, causing the Order Service to fail for 45 minutes.",
  "root_cause": "Connection pool limit reached due to unoptimised queries holding connections open.",
  "impact": "Order processing was fully unavailable for all users during the incident window.",
  "timeline_highlights": [
    "14:00 — Connection pool exhausted",
    "14:20 — Engineering team alerted",
    "14:45 — Service restored after pool reset"
  ],
  "generated_at": "2026-04-21T14:45:00Z",
  "is_fallback": false,
  "cache_hit": false
}
```

---

### POST /ai/recommend
Get 3 actionable recommendations for an incident.

**Request:**
```json
{
  "title": "Database Connection Pool Exhausted",
  "severity": "HIGH",
  "affected_systems": "PostgreSQL, Order Service",
  "root_cause": "Connection pool limit reached"
}
```

**Response:**
```json
{
  "recommendations": [
    {
      "action_type": "Hotfix",
      "description": "Increase connection pool size and add a connection timeout to prevent future exhaustion.",
      "priority": "HIGH"
    },
    {
      "action_type": "Monitoring",
      "description": "Set up alerts when connection pool usage exceeds 80%.",
      "priority": "HIGH"
    },
    {
      "action_type": "Communication",
      "description": "Notify affected teams and document the incident timeline.",
      "priority": "MEDIUM"
    }
  ],
  "is_fallback": false,
  "cache_hit": false
}
```

---

### POST /ai/generate-report
Generate a full structured incident report.

**Request:**
```json
{
  "title": "Database Connection Pool Exhausted",
  "severity": "HIGH",
  "description": "All DB connections were exhausted causing order processing to fail.",
  "affected_systems": "PostgreSQL, Order Service",
  "start_time": "2026-04-21 14:00",
  "end_time": "2026-04-21 14:45"
}
```

**Response:**
```json
{
  "title": "High Severity Database Outage — Connection Pool Exhaustion",
  "summary": "A connection pool exhaustion event caused a 45-minute outage of the Order Service on 21 April 2026.",
  "overview": "At 14:00, the PostgreSQL connection pool reached its maximum limit due to long-running queries holding connections open. This caused all new connection attempts from the Order Service to fail, resulting in a complete outage of order processing for all users until 14:45 when the pool was manually reset.",
  "key_items": [
    "Connection pool exhausted at 14:00",
    "Order Service fully unavailable for 45 minutes",
    "Root cause: unoptimised queries holding connections",
    "Manual pool reset resolved the issue"
  ],
  "recommendations": [
    "Increase connection pool size",
    "Add query timeout limits",
    "Set up connection pool usage alerts"
  ],
  "is_fallback": false,
  "generated_at": "2026-04-21T14:45:00Z"
}
```

---

## Fallback Behaviour

If the Groq API is unavailable, all endpoints return HTTP `200` with `"is_fallback": true` instead of an error — so the Java backend always gets a valid response.

## Caching

Responses are cached in Redis for 15 minutes using a SHA256 key. Cached responses include `"cache_hit": true`.

## Rate Limiting

All endpoints are limited to **30 requests per minute** per IP via `flask-limiter`.
