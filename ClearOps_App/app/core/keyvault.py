"""Loads secrets from Azure Key Vault or falls back to .env.local/.env for
local dev.

Local run vs. server run -- the two scopes this module switches between:
  - LOCAL:  .env.local (preferred) or .env is the ONLY source of config.
            Key Vault is never contacted, even if this machine has `az
            login` credentials cached (default USE_KEYVAULT=false below).
  - SERVER: k8s/helm/charts/clearops-backend/templates/deployment.yml sets
            USE_KEYVAULT=true as a plain Deployment env var, so every
            secret in SECRETS_MAP is pulled from Key Vault via the pod's
            AKS workload-identity managed identity instead.
"""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv

try:
    from azure.identity import DefaultAzureCredential
    from azure.keyvault.secrets import SecretClient

    _KEYVAULT_AVAILABLE = True
except ImportError:
    _KEYVAULT_AVAILABLE = False

logger = logging.getLogger(__name__)

APP_VERSION = os.getenv("APP_VERSION")

# app/core/keyvault.py -> app/core -> app -> backend/ (where .env.local/.env
# live). Resolved from this file's own location, NOT the current working
# directory -- so this works no matter where `uvicorn`/pytest/etc. is
# actually invoked from.
_BACKEND_DIR = Path(__file__).resolve().parents[2]
_ENV_LOCAL_PATH = _BACKEND_DIR / ".env.local"
_ENV_DEFAULT_PATH = _BACKEND_DIR / ".env"

# Key Vault secret names (hyphens) → environment variable names (underscores)
SECRETS_MAP = {
    "ALLOWED-HOSTS": "ALLOWED_HOSTS",
    "APP-ENV": "APP_ENV",
    "APP-NAME": "APP_NAME",
    "CORS-ORIGINS": "CORS_ORIGINS",
    "DATABASE-URL": "DATABASE_URL",
    "DB-DATABASE": "DB_DATABASE",
    "DB-PASSWORD": "DB_PASSWORD",
    "DB-SERVER": "DB_SERVER",
    "DB-USERNAME": "DB_USERNAME",
    "DEBUG": "DEBUG",
    # Azure AD (Entra ID) SSO login -- see app/core/msal_auth.py and
    # app/core/config.py. AZURE_REDIRECT_URI and DEFAULT_POST_LOGIN_REDIRECT_PATH
    # are not secrets, so they're set directly as Deployment env vars instead
    # (k8s/helm/charts/clearops-backend/templates/deployment.yml).
    "AZURE-TENANT-ID": "AZURE_TENANT_ID",
    "AZURE-CLIENT-ID": "AZURE_CLIENT_ID",
    "AZURE-CLIENT-SECRET": "AZURE_CLIENT_SECRET",
    "SESSION-SECRET-KEY": "SESSION_SECRET_KEY",
    # NOTE: "AZURE-REDIRECT-URI" is deliberately NOT mapped here even though
    # it may exist as a secret in Key Vault (harmless if so, just unused).
    # AZURE_REDIRECT_URI is set per-environment as a plain Deployment env var
    # instead (k8s/helm/charts/clearops-backend/templates/deployment.yml,
    # computed from each environment's own FRONTEND_URL). Every environment
    # (dev/qa/stage/prod) shares this same SECRETS_MAP but has its OWN Key
    # Vault + its OWN redirect domain -- if this were mapped, whatever single
    # value happens to be stored under "AZURE-REDIRECT-URI" in an
    # environment's Key Vault would silently overwrite/shadow the correct
    # per-environment Deployment value with zero warning, and any drift
    # between the two (wrong domain, trailing slash, http vs https, stale
    # copy-paste, etc.) breaks SSO with Microsoft rejecting the login
    # (AADSTS50011 redirect URI mismatch) instead of matching what's actually
    # registered on the Azure AD App Registration. Keep this single source
    # of truth in the Deployment env var only.
    # "AZURE-REDIRECT-URI": "AZURE_REDIRECT_URI",
    # Workday sync
    "workday-isu-int0233-password": "WORKDAY_ISU_INT0233_PASSWORD",
    "workday-isu-int0233-username": "WORKDAY_ISU_INT0233_USERNAME",
}


def load_env() -> None:
    """Load the local env file, then overlay secrets from Azure Key Vault
    when explicitly enabled.

    File choice: .env.local is preferred over .env when both exist -- this
    is what makes ".env.local" THE file for local dev (see module docstring).
    Only one of the two is ever loaded, never merged, so there's no
    ambiguity about which value wins.

    Key Vault values overwrite whatever the env file set, but ONLY when
    USE_KEYVAULT=true is explicitly present in the environment (server
    deployments set this; local dev never does, see below) -- missing/failed
    Key Vault access just leaves the env file's values in place, so this is
    always safe to call even without Azure credentials.
    """
    if _ENV_LOCAL_PATH.exists():
        load_dotenv(dotenv_path=_ENV_LOCAL_PATH)
        logger.info("Loaded local config from %s", _ENV_LOCAL_PATH.name)
    else:
        load_dotenv(dotenv_path=_ENV_DEFAULT_PATH)

    # Defaults to "false" -- Key Vault is opt-IN, not opt-out. A local run
    # must NEVER silently start pulling from Key Vault just because the
    # developer happens to have `az login` credentials cached on their
    # machine; only an explicit USE_KEYVAULT=true (set as a plain Deployment
    # env var on the server, see this module's docstring) turns it on.
    use_keyvault = os.getenv("USE_KEYVAULT", "false").lower() == "true"

    keyvault_url = os.getenv("KEYVAULT_URL", "https://shusedcrclearopskv01.vault.azure.net/")

    if use_keyvault and _KEYVAULT_AVAILABLE:
        try:
            client = SecretClient(
                vault_url=keyvault_url,
                # exclude_environment_credential=True is REQUIRED here:
                # AZURE_TENANT_ID/AZURE_CLIENT_ID/AZURE_CLIENT_SECRET (this
                # app's own SSO app-registration credentials, loaded from
                # .env just above) are the EXACT env var names azure-identity's
                # EnvironmentCredential also reads. Without excluding it,
                # DefaultAzureCredential silently authenticates to Key Vault
                # as the SSO app registration (which has no Key Vault
                # permissions) instead of this identity/managed identity, and
                # every secret lookup below fails with 403. Excluding it lets
                # DefaultAzureCredential fall through to
                # ManagedIdentityCredential/WorkloadIdentityCredential (in
                # AKS) or AzureCliCredential (local `az login`) instead.
                credential=DefaultAzureCredential(exclude_environment_credential=True),
            )

            loaded, skipped = 0, 0
            for kv_name, env_name in SECRETS_MAP.items():
                try:
                    os.environ[env_name] = client.get_secret(kv_name).value
                    loaded += 1
                except Exception:
                    skipped += 1
                    logger.debug("Secret not found in Key Vault, skipping: %s", kv_name)

            logger.info("Key Vault: %d secrets loaded, %d skipped", loaded, skipped)
        except Exception as exc:
            logger.exception("Key Vault unavailable, continuing with .env values: %s", exc)
    else:
        logger.info("Key Vault disabled (USE_KEYVAULT=%s) — using .env values only", use_keyvault)
