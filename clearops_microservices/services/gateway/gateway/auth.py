import os
from functools import lru_cache

import jwt
from fastapi import HTTPException, Request

TENANT_ID = os.getenv("AAD_TENANT_ID", "")
CLIENT_ID = os.getenv("AAD_CLIENT_ID", "")
AUTH_ENABLED = os.getenv("AUTH_ENABLED", "true").lower() == "true"


@lru_cache
def _jwks() -> jwt.PyJWKClient:
    return jwt.PyJWKClient(f"https://login.microsoftonline.com/{TENANT_ID}/discovery/v2.0/keys")


def authenticate(request: Request) -> dict | None:
    """Validate the Azure AD (Entra ID) bearer token issued after SSO."""
    if not AUTH_ENABLED:
        return None
    header = request.headers.get("authorization", "")
    if not header.lower().startswith("bearer "):
        raise HTTPException(401, "Missing bearer token")
    token = header[7:]
    try:
        key = _jwks().get_signing_key_from_jwt(token).key
        return jwt.decode(
            token, key, algorithms=["RS256"], audience=CLIENT_ID,
            issuer=f"https://login.microsoftonline.com/{TENANT_ID}/v2.0",
        )
    except jwt.PyJWTError:
        raise HTTPException(401, "Invalid token")
