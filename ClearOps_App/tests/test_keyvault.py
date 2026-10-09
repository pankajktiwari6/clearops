import importlib

import pytest

from app.core import keyvault


class FakeSecret:
    def __init__(self, value):
        self.value = value


class FakeClient:
    instances = []

    def __init__(self, vault_url, credential):
        self.vault_url, self.credential = vault_url, credential
        FakeClient.instances.append(self)

    def get_secret(self, name):
        if name == "DB-PASSWORD":
            return FakeSecret("from-vault")
        raise KeyError(name)  # every other secret is "missing"


@pytest.fixture()
def kv(tmp_path, monkeypatch):
    monkeypatch.setattr(keyvault, "_ENV_LOCAL_PATH", tmp_path / ".env.local")
    monkeypatch.setattr(keyvault, "_ENV_DEFAULT_PATH", tmp_path / ".env")
    for var in ("DB_PASSWORD", "DB_SERVER", "USE_KEYVAULT", "KEYVAULT_URL"):
        monkeypatch.delenv(var, raising=False)
    FakeClient.instances.clear()
    return tmp_path


def test_secrets_map_never_maps_redirect_uri():
    assert "AZURE-REDIRECT-URI" not in keyvault.SECRETS_MAP
    assert keyvault.SECRETS_MAP["DB-PASSWORD"] == "DB_PASSWORD"


def test_env_local_preferred_over_env(kv, monkeypatch):
    (kv / ".env").write_text("DB_SERVER=from-env\n")
    (kv / ".env.local").write_text("DB_SERVER=from-local\n")
    keyvault.load_env()
    assert keyvault.os.environ["DB_SERVER"] == "from-local"


def test_falls_back_to_env_when_no_local(kv):
    (kv / ".env").write_text("DB_SERVER=from-env\n")
    keyvault.load_env()
    assert keyvault.os.environ["DB_SERVER"] == "from-env"


def test_keyvault_not_contacted_by_default(kv, monkeypatch):
    monkeypatch.setattr(keyvault, "_KEYVAULT_AVAILABLE", True)
    monkeypatch.setattr(keyvault, "SecretClient", FakeClient, raising=False)
    keyvault.load_env()
    assert FakeClient.instances == []


def test_keyvault_overlays_env_file_and_skips_missing(kv, monkeypatch):
    (kv / ".env.local").write_text("DB_PASSWORD=from-file\nDB_SERVER=from-file\n")
    seen = {}

    def fake_cred(**kwargs):
        seen.update(kwargs)
        return object()

    monkeypatch.setenv("USE_KEYVAULT", "true")
    monkeypatch.setenv("KEYVAULT_URL", "https://vault.example/")
    monkeypatch.setattr(keyvault, "_KEYVAULT_AVAILABLE", True)
    monkeypatch.setattr(keyvault, "SecretClient", FakeClient, raising=False)
    monkeypatch.setattr(keyvault, "DefaultAzureCredential", fake_cred, raising=False)
    keyvault.load_env()
    assert keyvault.os.environ["DB_PASSWORD"] == "from-vault"      # vault wins
    assert keyvault.os.environ["DB_SERVER"] == "from-file"         # missing secret keeps file value
    assert FakeClient.instances[0].vault_url == "https://vault.example/"
    assert seen == {"exclude_environment_credential": True}


def test_keyvault_failure_keeps_env_values(kv, monkeypatch):
    (kv / ".env.local").write_text("DB_PASSWORD=from-file\n")

    def boom(**_):
        raise RuntimeError("no network")

    monkeypatch.setenv("USE_KEYVAULT", "true")
    monkeypatch.setattr(keyvault, "_KEYVAULT_AVAILABLE", True)
    monkeypatch.setattr(keyvault, "DefaultAzureCredential", boom, raising=False)
    monkeypatch.setattr(keyvault, "SecretClient", FakeClient, raising=False)
    keyvault.load_env()  # must not raise
    assert keyvault.os.environ["DB_PASSWORD"] == "from-file"
