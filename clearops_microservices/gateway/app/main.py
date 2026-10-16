import os

import httpx
from fastapi import FastAPI, Request, Response

ROUTES = {
    "users": os.getenv("USER_SERVICE_URL", "http://localhost:8001"),
    "orders": os.getenv("ORDER_SERVICE_URL", "http://localhost:8002"),
}

app = FastAPI(title="api-gateway", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.api_route("/api/{service}/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy(service: str, path: str, request: Request) -> Response:
    base = ROUTES.get(service)
    if base is None:
        return Response(b'{"detail":"Unknown service"}', 404, media_type="application/json")
    url = f"{base}/{service}" + (f"/{path}" if path else "")
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.request(
                request.method, url, params=request.query_params,
                content=await request.body(),
                headers={"content-type": request.headers.get("content-type", "application/json")},
            )
    except httpx.HTTPError:
        return Response(b'{"detail":"Upstream unavailable"}', 502, media_type="application/json")
    return Response(r.content, r.status_code, media_type=r.headers.get("content-type"))
