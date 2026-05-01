# 🚀 AI Gateway — Models-as-a-Service (MaaS)

> Production-grade AI infrastructure that intelligently routes requests across multiple models to optimize cost, latency, and scalability.

---

## 🧠 Overview

AI Gateway is a centralized **Models-as-a-Service (MaaS)** platform that abstracts multiple AI providers behind a single high-performance API.

Instead of directly calling one model, this system:

* Dynamically **routes requests** to the best model
* Balances **cost vs performance**
* Supports **hybrid AI (local + cloud)**
* Provides **rate limiting, caching, and usage analytics**

---

## ⚡ Key Features

### 🔐 Authentication & API Keys

* User signup & login system
* Secure password hashing (bcrypt)
* JWT-based authentication
* API key generation system
* API keys stored securely using:

  * Prefix + SHA256 hash (no raw key storage)
* API key revocation support (`is_active` flag)

---

### 🤖 Hybrid AI System (Core)

* Local model support via Ollama (CPU-based)
* Cloud model integration (Groq API)
* Unified response format across all models

---

### 🧠 Intelligent Routing Engine

* Decides which model to use based on:

  * Task complexity
  * Performance constraints
* Strategy:

  * Simple queries → Local model
  * Complex queries → Cloud model
* Built-in fallback:

  * Local → Cloud → Fail gracefully

---

### ⚡ Performance Optimization

#### 🔹 Rate Limiting (Redis)

* 100 requests/min per API key
* Prevents abuse & cost explosion
* Implemented using Redis counters

#### 🔹 Caching (Redis)

* Prompt-based caching
* SHA256 hash of request
* Instant response for repeated queries
* Reduces latency and cost

---

### 💰 Cost Tracking & Analytics

* Token-level usage tracking
* Per-request logging in PostgreSQL

#### Tracks:

* User ID
* Model used
* Provider (local/cloud)
* Input/output tokens
* Total tokens
* Latency
* Cost

---

### 📊 Usage API

* Endpoint: `/v1/usage`
* Provides:

  * Total requests
  * Total tokens
  * Total cost
  * Model usage breakdown

---

## 🏗️ Architecture

```
Client / App
     ↓
FastAPI Gateway (Auth + API Key)
     ↓
Rate Limiter (Redis)
     ↓
Cache Layer (Redis)
     ↓
Routing Engine (Core Brain)
     ↓
 ┌───────────────┬───────────────┐
 ↓               ↓
Local Model     Cloud Model
(Ollama)        (Groq API)
     ↓               ↓
     └────→ Unified Response ←────┘
             ↓
      Usage Logging (PostgreSQL)
             ↓
         Response
```

---

## 🔄 Request Flow

1. Client sends request with API key
2. API key is validated (prefix + hash match)
3. Rate limit check (Redis)
4. Cache lookup

   * If hit → return instantly
5. Routing engine decides model
6. Model executes (local or cloud)
7. Response normalized
8. Result cached
9. Usage logged (PostgreSQL)
10. Response returned

---

## 📂 Project Structure

```
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
│   └── api_keys.py
│
└── main.py
```

---

## 🔧 Tech Stack

| Layer                 | Technology   |
| --------------------- | ------------ |
| Backend               | FastAPI      |
| Database              | PostgreSQL   |
| Cache & Rate Limiting | Redis        |
| Local AI              | Ollama       |
| Cloud AI              | Groq API     |
| ORM                   | SQLAlchemy   |
| Auth                  | JWT + bcrypt |

---

## 🧪 API Endpoints

### 🔐 Auth

* `POST /signup`
* `POST /login`

---

### 🔑 API Keys

* `POST /api-keys/create`
* `GET /api-keys/list`
* `POST /api-keys/revoke`

---

### 🤖 AI

* `POST /v1/generate`

---

### 📊 Usage

* `GET /v1/usage`

---

## 📌 Example Request

```
POST /v1/generate
Authorization: Bearer <API_KEY>

{
  "prompt": "Explain Web3",
  "mode": "fast"
}
```

---

## 📌 Example Response

```
{
  "success": true,
  "provider": "cloud",
  "model": "llama-3.1-8b-instant",
  "response": "...",
  "metadata": {
    "latency_seconds": 0.5,
    "input_tokens": 50,
    "output_tokens": 60,
    "total_tokens": 110,
    "mode": "fast"
  }
}
```

---

## 🔐 Security Design

* Passwords hashed using bcrypt
* API keys:

  * Never stored in raw form
  * Stored as prefix + SHA256 hash
* JWT-based authentication
* API key revocation supported

---

## 🚀 Why This Project Stands Out

This is not a basic AI app — it is **AI infrastructure**.

### Demonstrates:

* System design thinking
* Scalability & performance optimization
* Multi-model orchestration
* Production-grade backend engineering

---

## 📈 Current Status

✅ Authentication system
✅ API key management (secure)
✅ Hybrid AI (local + cloud)
✅ Intelligent routing engine
✅ Rate limiting (Redis)
✅ Caching layer (Redis)
✅ Usage analytics API

---

## 🔜 Upcoming Features

* RAG (Retrieval Augmented Generation)
* Agentic workflows (multi-step reasoning)
* Dockerization & cloud deployment
* Observability dashboard (metrics + logs) for both user and admin

---

## 🧠 One-Line Summary

> A production-grade AI Gateway that intelligently routes requests across local and cloud models with built-in cost optimization, caching, rate limiting, and usage tracking.

---

## ⭐ If you find this useful

Give it a ⭐ and feel free to contribute or fork!

---
