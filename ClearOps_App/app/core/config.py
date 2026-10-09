from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.keyvault import load_env

# Loads .env.local (preferred) or .env, then overlays secrets fetched from
# Azure Key Vault ONLY when USE_KEYVAULT=true (per keyvault.SECRETS_MAP)
# into os.environ -- MUST run before Settings() below is instantiated, since
# pydantic-settings prioritizes real environment variables over any env
# file, so this is how Key Vault values actually end up "winning" here when
# enabled+reachable (falling back to the local env file otherwise). See
# app.core.keyvault's module docstring for the full local-vs-server split.
load_env()


class Settings(BaseSettings):
    APP_NAME: str = "Backend API"
    APP_ENV: str = "development"
    DEBUG: bool = False

    DB_SERVER: str
    DB_DATABASE: str

    # LOCAL: set directly in .env.local (required there -- Key Vault is
    # never contacted locally, see app.core.keyvault).
    # SERVER: left unset in every env file; app.core.keyvault.load_env()
    # (called above) overlays them from Azure Key Vault's
    # DB-USERNAME/DB-PASSWORD secrets since USE_KEYVAULT=true there.
    DB_USERNAME: str | None = None
    DB_PASSWORD: str | None = None

    KEY_VAULT_URL: str

    # ---- Azure AD (Entra ID) SSO login --------------------------------------
    # All values come from .env (gitignored) -- never hardcode these. To
    # source AZURE_CLIENT_SECRET from Key Vault instead, add an
    # "AZURE-CLIENT-SECRET" -> "AZURE_CLIENT_SECRET" entry to
    # app.core.keyvault.SECRETS_MAP.
    #
    # NOTE: AZURE_TENANT_ID/AZURE_CLIENT_ID/AZURE_CLIENT_SECRET are ALSO the
    # exact env var names the Azure SDK's DefaultAzureCredential looks for
    # (EnvironmentCredential), and that AKS workload identity auto-injects
    # for the pod's managed identity. app.core.keyvault.load_env() explicitly
    # excludes EnvironmentCredential when building DefaultAzureCredential for
    # Key Vault access specifically to avoid these colliding -- see the
    # comment there before changing either of these.
    AZURE_TENANT_ID: str | None = None
    AZURE_CLIENT_ID: str | None = None
    AZURE_CLIENT_SECRET: str | None = None
    AZURE_REDIRECT_URI: str = "http://localhost:8000/callback"
    AZURE_SCOPES: list[str] = ["User.Read"]

    # Where to send the browser after a successful/failed login. FRONTEND_URL
    # is the app's origin; DEFAULT_POST_LOGIN_REDIRECT_PATH is the in-app page
    # to land on (can be overridden per-login via ?redirect_to=/some/path on
    # GET /api/auth/v1/login, e.g. redirect_to=/reports/budget-analysis).
    FRONTEND_URL: str = "http://localhost:8000"
    # NOTE: this must NEVER be "/callback" -- that's the technical OAuth
    # callback route itself, not an in-app landing page. If it ever resolves
    # there (e.g. this env var is missing at runtime), the browser gets
    # redirected back to the callback URL after login instead of a real in-app
    # page, breaking the "authenticate then land in the app" flow.
    DEFAULT_POST_LOGIN_REDIRECT_PATH: str = "/"

    # Signs the session cookie that carries the OAuth state + logged-in user
    # between /login, /callback and subsequent requests. Must be set to a real
    # random value in .env -- generate one with:
    #   python -c "import secrets; print(secrets.token_hex(32))"
    SESSION_SECRET_KEY: str = ""

    ALLOWED_HOSTS: list[str] = []
    CORS_ORIGINS: list[str] = []

    # ---- Caching / refresh cron ---------------------------------------------
    # CACHE_REFRESH_CRON_MINUTES: how often app.core.scheduler reloads every
    # full-table snapshot (app.core.data_store) and clears cached report
    # results (app.core.cache). Max data staleness == this interval.
    # CACHE_TTL_SECONDS: safety-net expiry for report results; keep it equal
    # to the cron interval (the cron normally clears them first anyway).
    CACHE_TTL_SECONDS: int = 600           # 10 minutes
    CACHE_MAX_ENTRIES: int = 512
    CACHE_REFRESH_CRON_MINUTES: int = 10

    model_config = SettingsConfigDict(
        # Belt-and-suspenders fallback only -- app.core.keyvault.load_env()
        # (called above, before this class is ever instantiated) already
        # loads .env.local (preferred) or .env directly into os.environ via
        # python-dotenv, and real os.environ values always take priority over
        # anything pydantic-settings would read from these files itself. On
        # the server, neither file is deployed at all (config comes from
        # plain Deployment env vars + Key Vault, see deployment.yml), so this
        # is a no-op there.
        env_file=(".env", ".env.local"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # .env(.local) also carries DB_USERNAME/DB_PASSWORD/DB_SERVER/DB_DATABASE,
                          # which app.core.database reads directly (not through this Settings
                          # model) -- without this, Settings() raises on those extra keys and
                          # the app fails to boot at all.
    )


settings = Settings()
