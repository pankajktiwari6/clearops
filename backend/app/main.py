from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.crud import MAPPING, build_routers
from app.core.config import settings

app = FastAPI(title="ClearOps API", version="0.1.0")
app.add_middleware(
    CORSMiddleware, allow_origins=settings.CORS_ORIGINS, allow_methods=["*"], allow_headers=["*"]
)

for router in build_routers():
    app.include_router(router, prefix="/api")


@app.get("/health", tags=["meta"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/column-mapping", tags=["meta"])
def column_mapping() -> dict:
    """Frontend field <-> ORM attribute <-> DB column mapping."""
    return MAPPING
