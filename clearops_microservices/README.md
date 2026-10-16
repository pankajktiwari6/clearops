# ClearOps Microservices

| Service | Port | Role |
|---|---|---|
| gateway | 8000 | Single entry point; proxies `/api/users/*` and `/api/orders/*` |
| user-service | 8001 | User CRUD (in-memory store) |
| order-service | 8002 | Orders; validates the user via HTTP call to user-service |

## Run
    docker compose up --build
    curl -X POST localhost:8000/api/users/ -H 'content-type: application/json' -d '{"name":"Ada","email":"ada@example.com"}'
    curl -X POST localhost:8000/api/orders/ -H 'content-type: application/json' -d '{"user_id":1,"item":"pen","quantity":2}'

Each service also exposes `/docs` (Swagger) when run directly: `cd user_service && uvicorn app.main:app --port 8001`.

## Test
    pip install -r gateway/requirements.txt -r user_service/requirements.txt -r order_service/requirements.txt pytest
    pytest

## Next steps
Swap the in-memory stores for per-service databases, add auth at the gateway, and add a message broker for async events.
