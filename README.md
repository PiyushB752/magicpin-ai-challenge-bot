# Magicpin AI Challenge Bot

A deterministic merchant engagement bot built for the Magicpin AI Challenge.

The solution is intentionally lightweight, context-aware, and entirely in-memory, following the challenge requirements of keeping the implementation small, deterministic, and easy to replay.

## Features

* FastAPI-based API service
* In-memory stores
* Merchant, customer, category and trigger context support
* Context versioning
* Stale version rejection
* Trigger prioritization
* Deterministic recommendation generation
* Deterministic reply generation
* Replay-friendly behavior
* No databases
* No LLMs
* No embeddings
* No vector stores

## Tech Stack

* Python
* FastAPI
* Pydantic
* Uvicorn

## Project Structure

```
magicpin-ai-challenge/

app.py
store.py
engine.py
requirements.txt

composers/
handlers/
services/
utils/

dataset/
├── customers_seed.json
├── merchants_seed.json
├── triggers_seed.json
└── categories/
    ├── dentists.json
    ├── gyms.json
    ├── pharmacies.json
    ├── restaurants.json
    └── salons.json

examples/

challenge-brief.md
challenge-testing-brief.md
engagement-design.md
engagement-research.md
```

## Installation

Clone the repository.

```
git clone https://github.com/PiyushB752/magicpin-ai-challenge-bot.git
```

Install dependencies.

```
pip install -r requirements.txt
```

Start the application.

```
uvicorn app:app --reload
```

API documentation:

```
http://localhost:8000/docs
```

## API Endpoints

### Health

```
GET /v1/healthz
```

Returns service health information.

### Metadata

```
GET /v1/metadata
```

Returns service metadata and dataset statistics.

### Merchant

```
GET /v1/merchant/{merchant_id}
```

Fetch merchant details.

### Customer

```
GET /v1/customer/{customer_id}
```

Fetch customer details.

### Trigger

```
GET /v1/trigger/{trigger_id}
```

Fetch trigger details.

### Merchant Customers

```
GET /v1/merchant/{merchant_id}/customers
```

Returns customers associated with a merchant.

### Merchant Triggers

```
GET /v1/merchant/{merchant_id}/triggers
```

Returns triggers associated with a merchant.

### Context

Save context.

```
POST /v1/context
```

Example request:

```
{
  "entity_type": "merchant",
  "entity_id": "m_001",
  "version": 1,
  "payload": {}
}
```

Supported entity types:

* merchant
* customer
* category
* trigger

If the incoming version is stale:

```
{
  "accepted": false,
  "reason": "stale_version",
  "current_version": 1
}
```

Successful response:

```
{
  "accepted": true,
  "ack_id": "ack_merchant_m_001_v1",
  "stored_at": "2026-07-03T12:00:00Z"
}
```

Read context.

```
GET /v1/context/{entity_type}/{entity_id}
```

### Tick

```
POST /v1/tick
```

Determines the highest priority trigger for a merchant and generates a deterministic recommendation.

Example:

```
{
  "merchant_id": "m_001"
}
```

### Reply

```
POST /v1/reply
```

Generates deterministic merchant responses.

Example:

```
{
  "merchant_id": "m_001",
  "message": "renew my subscription"
}
```

## Trigger Prioritization

Triggers are scored deterministically.

Example priorities:

* supply_alert
* renewal_due
* perf_dip
* active_planning_intent
* review_theme_emerged
* trial_followup
* festival_upcoming
* research_digest

The highest scoring trigger is selected during tick execution.

## Design Principles

This project intentionally avoids:

* LLMs
* Embeddings
* LangChain
* Redis
* PostgreSQL
* MongoDB
* Vector databases
* External AI APIs

All state is maintained using Python dictionaries.

The objective is to provide a simple, deterministic, replay-friendly implementation suitable for evaluation environments.

## Running Tests

Open Swagger UI.

```
http://localhost:8000/docs
```

Validate:

```
GET  /
GET  /v1/healthz
GET  /v1/metadata
GET  /v1/merchant/{id}
GET  /v1/customer/{id}
GET  /v1/trigger/{id}
GET  /v1/merchant/{id}/customers
GET  /v1/merchant/{id}/triggers
POST /v1/context
GET  /v1/context/{entity_type}/{entity_id}
POST /v1/tick
POST /v1/reply
```

## Deployment

Required public endpoints:

```
POST /v1/context
POST /v1/tick
POST /v1/reply
GET /v1/healthz
GET /v1/metadata
```