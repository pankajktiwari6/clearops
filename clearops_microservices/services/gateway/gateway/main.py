import os

import httpx
from fastapi import Depends, FastAPI, Request, Response

from . import cache
from .auth import authenticate
from .telemetry import setup_telemetry

setup_telemetry()

# /api/<domain>/<table>[/<key>]  ->  <domain service>/api/<table>[/<key>]
ROUTES = {
    "setup": os.getenv("SETUP_SERVICE_URL", "http://localhost:8001"),
    "timeplanner": os.getenv("TIMEPLANNER_SERVICE_URL", "http://localhost:8002"),
    "project": os.getenv("PROJECT_SERVICE_URL", "http://localhost:8003"),
    "admin": os.getenv("ADMIN_SERVICE_URL", "http://localhost:8004"),
}
JSON = "application/json"
DEV_USER_EMAIL = os.getenv("DEV_USER_EMAIL", "")  # only used when AUTH_ENABLED=false (local development)


def login_email(claims: dict | None) -> str:
    """Email of the signed-in user, taken from the validated Azure AD token (never from the client)."""
    if claims:
        return claims.get("email") or claims.get("preferred_username") or claims.get("upn") or ""
    return DEV_USER_EMAIL

app = FastAPI(title="api-gateway", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.api_route("/api/{service}/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy(service: str, path: str, request: Request, claims=Depends(authenticate)) -> Response:
    base = ROUTES.get(service)
    if base is None:
        return Response(b'{"detail":"Unknown service"}', 404, media_type=JSON)
    url = f"{base}/api/{path}"
    key = f"cache:{service}:{path}?{request.url.query}"
    is_read = request.method == "GET"
    if is_read and (hit := await cache.get(key)):
        return Response(hit, 200, media_type=JSON, headers={"x-cache": "HIT"})
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.request(
                request.method, url, params=request.query_params, content=await request.body(),
                headers={"content-type": request.headers.get("content-type", JSON),
                         "x-user-email": login_email(claims)},  # identity for the domain services
            )
    except httpx.HTTPError:
        return Response(b'{"detail":"Upstream unavailable"}', 502, media_type=JSON)
    if is_read and r.status_code == 200:
        await cache.put(key, r.content)
    elif not is_read and r.is_success:
        await cache.invalidate(f"cache:{service}:")
    return Response(r.content, r.status_code, media_type=r.headers.get("content-type"))
