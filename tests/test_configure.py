import pytest
from typer.testing import CliRunner
from app.commands.configure import app
from unittest.mock import patch
from pathlib import Path

runner = CliRunner()


def _make_prepared_dir(tmp_path: Path) -> Path:
    d = tmp_path / "prepared"
    d.mkdir()
    for name in ("db_init", "keycloak", "nginx"):
        (d / name).mkdir()
    (d / "docker-compose.yaml").write_text("version: '3'\nservices: {}\n")
    return d

def test_configure_env(tmp_path, monkeypatch):
    work = _make_prepared_dir(tmp_path)
    monkeypatch.chdir(work)  # check_prepared() looks in CWD
    
    result = runner.invoke(app, [
        "--postgres-password", "Abcdef!1",
        "--keycloak-admin-password", "Abcdef!1",
        "--identity-hostname", "identity.test.local",
        "--migrants-hostname", "migrants.test.local",
        "--pa-hostname", "pa.test.local",
        "--ngo-hostname", "ngo.test.local",
        "--traefik-acme-email", "test@example.com",
        "--traefik-hostname", "traefik.test.local",
        "--git-hostname", "git.test.local",
        "--gitea-db-password", "Abcdef!1",
        "--weblate-email-host", "smtp.test.local",
        "--weblate-email-host-user", "weblate_user",
        "--weblate-server-email", "weblate@test.local",
        "--weblate-default-from-email", "weblate@test.local",
        "--weblate-admin-password", "Abcdef!1",
        "--weblate-admin-email", "weblate_admin@test.local",
        "--translation-hostname", "translation.test.local",
        "--weblate-postgres-password", "Abcdef!1",
        "--timezone", "Europe/Berlin",
        "--micado-db-password", "Abcdef!1",
        "--weblate-email-host-password", "Abcdef!1",
        "--algorithm-password", "Abcdef!1",
        "--micado-weblate-key", "test_micado_weblate_key",
        "--portainer-hostname", "portainer.test.local",
        "--api-hostname", "api.test.local",
    ])
    assert result.exit_code == 0, result.output
    assert ".env" in "\n".join(work.iterdir().__str__() for _ in [0]) or (work / ".env").exists()

    assert "Configuring MICADO application" in result.output

if __name__ == "__main__":
    pytest.main()
