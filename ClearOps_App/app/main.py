from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.crud import MAPPING, build_routers
from app.api.stp import router as stp_router
from app.core.config import settings

def create_app(title: str = "ClearOps_App", tables: set[str] | None = None) -> FastAPI:
    """The full API, or one microservice's slice of it (`tables` = mapping keys it owns)."""
    app = FastAPI(title=title, version="0.1.0")
    app.add_middleware(
        CORSMiddleware, allow_origins=settings.CORS_ORIGINS, allow_methods=["*"], allow_headers=["*"]
    )
    for router in build_routers(tables):
        app.include_router(router, prefix="/api")
    if tables is None or "ProjectSTP" in tables:
        app.include_router(stp_router, prefix="/api")

    @app.get("/health", tags=["meta"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/api/column-mapping", tags=["meta"])
    def column_mapping() -> dict:
        """Frontend field <-> ORM attribute <-> DB column mapping (this service's tables)."""
        return {k: v for k, v in MAPPING.items() if tables is None or k in tables}

    return app


app = create_app()
