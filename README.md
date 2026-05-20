# 🚀 AI Gateway — Models-as-a-Service (MaaS)

<p align="center">
  <img src="assets/Home.png" width="850"/>
</p>

> Production-grade AI infrastructure that unifies local and cloud LLMs behind a single API with intelligent routing, secure API keys, rate limiting, caching, usage analytics, and a Streamlit frontend.

---

## 🧠 Overview

AI Gateway is a full-stack **Models-as-a-Service (MaaS)** platform that abstracts multiple AI providers behind one production-grade API.

Instead of hardcoding a single LLM, this platform:

- Dynamically routes requests to the optimal model
- Balances cost, latency, and response quality
- Supports hybrid inference (local + cloud)
- Provides secure API key management
- Enforces rate limits
- Caches responses
- Tracks usage and costs
- Offers an interactive Streamlit UI


---

[WATCH THE DEMO](https://drive.google.com/file/d/11BIwEJm8U8ZgiBqWG5-jepaljv3wUQ8K/view?usp=sharing)

---

# ✨ Key Features

## 🔐 Authentication & Authorization

- User signup and login
- Password hashing with `bcrypt`
- JWT-based authentication
- Secure API key generation
- API key hashing using SHA-256
- API key revocation (`is_active = False`)

---

## 🔑 API Key Management

Each user can:

- Generate multiple API keys
- List all active keys
- Revoke compromised keys instantly
- Select API keys from the frontend

API keys are stored securely as:

- Key prefix (e.g., `agw_ab12cd`)
- SHA-256 hash

Raw keys are shown only once at creation.

---

## 🤖 Hybrid AI Inference

### Local Models
Powered by : Ollama

Examples:
- `phi3`
- `mistral`
- `llama3`

### Cloud Models
Powered by : Groq

Examples:
- `llama-3.1-8b-instant`
- `llama-3.3-70b-versatile`

---

## 🧠 Intelligent Routing Engine

Automatically selects the best model based on:

- Task complexity
- Latency requirements
- Cost constraints
- Provider availability

### Example Strategy

| Mode       | Preferred Provider |
|----------: |-------------------|
| fast       | Groq Cloud |
| balanced   | Local → Cloud fallback |
| detailed   | Local or Cloud |

---

## 🔄 Fallback Mechanism

If the selected model fails:

1. Retry alternate provider
2. Return graceful error if all providers fail

---

## ⚡ Rate Limiting (Redis)

- 100 requests/minute per API key
- Prevents abuse and runaway costs

Implemented using Redis.

---

## ⚡ Response Caching (Redis)

- Prompt + mode hashed with SHA-256
- Cached responses returned instantly
- Reduces latency and cloud costs

---

## 💰 Usage Tracking & Cost Analytics

Every request is logged to PostgreSQL.

Tracked fields:

- User ID
- API Key ID
- Model
- Provider
- Input tokens
- Output tokens
- Total tokens
- Latency
- Cost
- Cache hit flag
- Timestamp

---

## 📊 Usage Analytics API

Endpoint:

```http
GET /v1/usage
````

Returns:

* Total requests
* Total tokens
* Total cost
* Average latency
* Model usage breakdown
* Recent requests

---

## 🌐 Streamlit Frontend

Built using Streamlit.

Includes:

* Login / Signup
* API Key Management
* AI Playground with live streaming responses
* Usage Analytics Dashboard
* Admin Dashboard (foundation)

---

## 📡 Server-Sent Events (Streaming)

Responses stream token-by-token like ChatGPT.

Frontend displays:

* Live generation
* Final clean response
* Metadata (latency, tokens, model)

---

# 🏗️ Architecture

```text
                ┌───────────────────────────────┐
                │       Streamlit Frontend      │
                └───────────────┬───────────────┘
                                │
                                ▼
                ┌───────────────────────────────┐
                │        FastAPI Gateway        │
                │ JWT Auth + API Key Validation │
                └───────────────┬───────────────┘
                                │
                                ▼
                ┌───────────────────────────────┐
                │      Rate Limiter (Redis)     │
                └───────────────┬───────────────┘
                                │
                                ▼
                ┌───────────────────────────────┐
                │       Cache Layer (Redis)     │
                └───────────────┬───────────────┘
                                │
                                ▼
                ┌───────────────────────────────┐
                │   Intelligent Router Engine   │
                └───────────────┬───────────────┘
                                │
                  ┌─────────────┴─────────────┐
                  ▼                           ▼
        ┌──────────────────┐       ┌────────────────────┐
        │ Local Models     │       │ Cloud Models       │
        │ Ollama           │       │ Groq API           │
        └────────┬─────────┘       └─────────┬──────────┘
                 └──────────────┬────────────┘
                                ▼
                ┌───────────────────────────────┐
                │     Unified Response Layer    │
                └───────────────┬───────────────┘
                                ▼
                ┌───────────────────────────────┐
                │ Usage Logging (PostgreSQL)    │
                └───────────────────────────────┘
```

---

# 🔄 End-to-End Request Flow

1. User logs in.
2. User generates API key.
3. Client sends prompt with `x-api-key`.
4. API key validated.
5. Rate limit check.
6. Cache lookup.
7. Router selects model.
8. Model generates response.
9. Tokens stream to client.
10. Response cached.
11. Usage logged.
12. Analytics updated.

---

# 📂 Project Structure

```text
app/
├── core/
│   ├── config.py
│   ├── redis_client.py
│   └── security.py
│
├── db/
│   ├── database.py
│   └── models.py
│
├── services/
│   ├── auth_service.py
│   ├── api_key_service.py
│   ├── local_model.py
│   ├── cloud_model.py
│   └── router.py
│
├── routes/
│   ├── auth.py
│   ├── api_keys.py
│   └── generate.py
│
├── schemas/
│   ├── users.py
│   ├── api_keys.py
│   └── generate.py
│
├── frontend/
│   ├── Home.py
│   ├── utils.py
│   └── pages/
│       ├── 1_Login.py
│       ├── 2_API_Keys.py
│       ├── 3_AI_Playground.py
│       ├── 4_Usage_Analytics.py
│       └── 5_Admin_Dashboard.py
│
└── main.py
```

---

# 🛠️ Tech Stack

| Layer          | Technology         |
| -------------- | ------------------ |
| Backend API    | Python / FastAPI   |
| Frontend       | Streamlit          |
| Database       | PostgreSQL         |
| Cache          | Redis              |
| ORM            | SQLAlchemy         |
| Authentication | JWT + bcrypt       |
| Local LLMs     | Ollama             |
| Cloud LLMs     | Groq API           |

---

# 📡 API Endpoints

## Authentication

* `POST /signup`
* `POST /login`

## API Keys

* `POST /api-keys/create`
* `GET /api-keys/list`
* `POST /api-keys/revoke`

## AI

* `POST /v1/generate`

## Analytics

* `GET /v1/usage`

---

# 📌 Example Request

```http
POST /v1/generate
x-api-key: agw_xxxxxxxxxxxxxxxxxxxxxxxxxx
Content-Type: application/json

{
  "prompt": "Explain Web3 like I’m 10 years old.",
  "mode": "fast"
}
```

---

# 📌 Example Response (Streaming)

```text
data: {"token":"Web3"}
data: {"token":" is"}
data: {"token":" the"}
...
data: [DONE]
```

---

# 🔐 Security Design

* Passwords hashed using bcrypt
* API keys hashed using SHA-256
* JWT authentication
* API key revocation
* Per-key rate limiting

---

# 🚀 Getting Started

## 1. Clone Repository

```bash
git clone https://github.com/your-username/ai-gateway.git
cd ai-gateway
```

## 2. Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure Environment Variables

Create `.env`:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/ai_gateway
SECRET_KEY=your_super_secret_key
GROQ_API_KEY=your_groq_api_key
REDIS_URL=redis://localhost:6379/0
```

## 5. Start PostgreSQL

Ensure PostgreSQL is running and database `ai_gateway` exists.

## 6. Start Redis

```bash
redis-server
```

## 7. Start Ollama

```bash
ollama serve
ollama pull phi3
```

## 8. Run FastAPI Backend

```bash
uvicorn app.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

## 9. Run Streamlit Frontend

```bash
cd app/frontend
streamlit run Home.py
```

Frontend URL:

```text
http://localhost:8501
```

---

# 🐳 Run with Docker (Upcoming)

Docker support is planned.

Future deployment stack:

* FastAPI
* Streamlit
* PostgreSQL
* Redis
* Ollama

---

# 📈 Current Status

* ✅ Authentication system
* ✅ Secure API key management
* ✅ Hybrid local + cloud AI
* ✅ Intelligent routing
* ✅ Streaming responses
* ✅ Redis rate limiting
* ✅ Redis caching
* ✅ Usage analytics
* ✅ Streamlit frontend

---

# 🔮 Upcoming Features

* 📚 Retrieval-Augmented Generation (RAG)
* 🤖 Agentic workflows with LangGraph
* 🐳 Docker & Docker Compose
* ☁️ Cloud deployment
* 📊 Advanced admin dashboard
* 🔍 Observability and tracing

---

# 🏆 Why This Project Stands Out

This project demonstrates:

* Production-grade backend engineering
* System design skills
* Multi-model orchestration
* Cost optimization
* Security best practices
* SaaS platform architecture
* AI infrastructure development

---

# 🧠 One-Line Summary

> A full-stack AI infrastructure platform that intelligently routes prompts across multiple LLM providers while handling authentication, rate limiting, caching, analytics, and live streaming responses.

---

# ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.

```
