"""Environment loading: local env file, optionally overlaid by Azure Key Vault.

LOCAL   : .env.local (preferred) or .env is loaded into os.environ via
          python-dotenv. Key Vault is never contacted (USE_KEYVAULT unset/false).
SERVER  : no env file is deployed; plain Deployment env vars supply config and
          USE_KEYVAULT=true makes load_env() overlay the secrets in SECRETS_MAP
          from Key Vault (KEY_VAULT_URL) into os.environ. If Key Vault is
          unreachable, startup continues with whatever is already in the
          environment.
"""
import logging
import os
from pathlib import Path

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Key Vault secret name -> environment variable name.
SECRETS_MAP: dict[str, str] = {
    "DB-USERNAME": "DB_USERNAME",
    "DB-PASSWORD": "DB_PASSWORD",
}


def _load_env_file() -> None:
    for name in (".env.local", ".env"):
        path = Path(name)
        if path.is_file():
            # override=False: real environment variables keep priority.
            load_dotenv(path, override=False)
            return


def _overlay_key_vault() -> None:
    url = os.environ.get("KEY_VAULT_URL")
    if not url:
        logger.warning("USE_KEYVAULT=true but KEY_VAULT_URL is not set; skipping Key Vault")
        return
    try:
        from azure.identity import DefaultAzureCredential
        from azure.keyvault.secrets import SecretClient

        # EnvironmentCredential is excluded on purpose: AZURE_TENANT_ID /
        # AZURE_CLIENT_ID / AZURE_CLIENT_SECRET in this app are the SSO login
        # app registration, NOT the identity that may read Key Vault. Letting
        # the SDK pick them up would authenticate to Key Vault as the wrong
        # principal (workload identity / managed identity are still tried).
        credential = DefaultAzureCredential(exclude_environment_credential=True)
        client = SecretClient(vault_url=url, credential=credential)
        for secret_name, env_name in SECRETS_MAP.items():
            os.environ[env_name] = client.get_secret(secret_name).value or ""
    except Exception:  # noqa: BLE001 - fall back to the env file/env vars
        logger.exception("Key Vault unreachable; falling back to existing environment")


def load_env() -> None:
    _load_env_file()
    if os.environ.get("USE_KEYVAULT", "").lower() == "true":
        _overlay_key_vault()
