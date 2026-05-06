# 🤖 AI Service – Summary Card

## 📌 Project Overview
AI-powered backend service that answers user queries securely using a language model.

---

## 🔌 API Endpoints

### 1. POST /ask_ai
- Input: User question
- Output: AI-generated response
- Features:
  - Input validation
  - Prompt injection protection
  - Rate limiting

---

### 2. GET /health
- Returns service status
- Used for monitoring

---

### 3. (Internal) Security Layer
- Sanitization
- Prompt guard
- Error handling

---

## 🛠 Tech Stack

- **Backend:** Flask (Python)
- **AI Model:** Groq API
- **Testing:** Pytest
- **Security:** OWASP ZAP, Flask-Limiter
- **Container (optional):** Docker

---

## 🔐 Key Features

- Prevents SQL Injection  
- Blocks Prompt Injection  
- Rate limiting for abuse control  
- Secure headers implemented  
- No personal data (PII safe)  

---

## 🧪 Testing & Validation

- ✅ 8 unit tests (pytest)
- ✅ OWASP ZAP security scan
- ✅ AI quality score ≥ 4/5
- ✅ End-to-end testing completed

---

## 📂 GitHub Repository

https://github.com/sukkibhat9887-code/incident-timeline-visualiser

---

## 👩‍💻 Developer

Sukrutha S. Bhat

---

## 🚀 Status

✔ Secure  
✔ Tested  
✔ Demo-ready  