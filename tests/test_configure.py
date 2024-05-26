import pytest
from typer.testing import CliRunner
from app.commands.configure import app

runner = CliRunner()

def test_configure_env():
    result = runner.invoke(app, [
        "environment",
        "--postgres-password", "test_postgres_password",
        "--keycloak-admin-password", "test_keycloak_admin_password",
        "--identity-hostname", "identity.test.local",
        "--migrants-hostname", "migrants.test.local",
        "--pa-hostname", "pa.test.local",
        "--ngo-hostname", "ngo.test.local",
        "--analytic-hostname", "analytics.test.local",
        "--traefik-acme-email", "test@example.com",
        "--traefik-hostname", "traefik.test.local",
        "--git-hostname", "git.test.local",
        "--gitea-db-password", "test_gitea_db_password",
        "--weblate-email-host", "smtp.test.local",
        "--weblate-email-host-user", "weblate_user",
        "--weblate-server-email", "weblate@test.local",
        "--weblate-default-from-email", "weblate@test.local",
        "--weblate-admin-password", "test_weblate_admin_password",
        "--weblate-admin-email", "weblate_admin@test.local",
        "--translation-hostname", "translation.test.local",
        "--weblate-postgres-password", "test_weblate_postgres_password",
        "--timezone", "Europe/Berlin",
        "--rocketchat-hostname", "rocketchat.test.local",
        "--rocketchat-admin-password", "test_rocketchat_admin_password",
        "--countly-migrants-app-id", "test_countly_migrants_app_id",
        "--countly-migrants-api-key", "test_countly_migrants_api_key",
        "--micado-db-password", "test_micado_db_password",
        "--weblate-email-host-password", "test_weblate_email_host_password",
        "--countly-admin-password", "test_countly_admin_password",
        "--algorithm-password", "test_algorithm_password",
        "--micado-weblate-key", "test_micado_weblate_key",
        "--portainer-hostname", "portainer.test.local",
    ])
    assert result.exit_code == 0
    assert "Configuring MICADO application" in result.output

if __name__ == "__main__":
    pytest.main()
