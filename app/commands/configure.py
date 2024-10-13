from password_validator import PasswordValidator
import app.core.checks as checks
import typer
import re
from jinja2 import Template
from typing_extensions import Annotated
from app.core.fileops import create_folder


def configure_env(template_str, env_vars, output_file=".env"):
    """
    Generate a .env file from a template string and a corresponding dictionary of variables.

    Args:
    template_str (str): The .env template as a string.
    env_vars (dict): A dictionary containing the variables to replace in the template.
    output_file (str): The output file name (default is '.env').

    Returns:
    None
    """
    template = Template(template_str)
    rendered_env = template.render(env_vars)
    with open(output_file, "w") as f:
        f.write(rendered_env)
    print(f"Generated {output_file} file successfully!")


def pwd_callback(value: str) -> str:
    """
    Validates a password input using the PasswordValidator schema.

    Args:
        value (str): The password to validate.

    Returns:
        str: The validated password.

    Raises:
        typer.BadParameter: If the password is empty or does not meet the validation rules.
    """
    # print("Validating password")
    if not value:
        raise typer.BadParameter("Password cannot be empty")
    schema = PasswordValidator()
    schema.min(6).max(
        10
    ).has().uppercase().has().lowercase().has().digits().has().no().spaces()
    validation = schema.validate(value)
    # print(f"Validation was : {validation}")
    if not validation:
        raise typer.BadParameter(
            "Password do not respect validation rules: must be between 6 and 10 characters, must contain at least one uppercase, lowercase, digit and special character"
        )
    return value


def email_callback(value: str) -> str:
    """
    Validates an email address input and returns the value if it is valid.

    Args:
        value (str): The email address to validate.

    Returns:
        str: The valid email address.

    Raises:
        typer.BadParameter: If the input email address is not in a valid format.
    """
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_regex, value):
        raise typer.BadParameter("Invalid email format")
    return value


def hostname_callback(value: str) -> str:
    """
    Validates and returns a hostname string.

    Args:
        value (str): The hostname to validate.

    Returns:
        str: The validated hostname.

    Raises:
        typer.BadParameter: If the provided hostname is invalid.
    """
    hostname_regex = r"^(?=.{1,255}$)[0-9A-Za-z]([0-9A-Za-z-]{0,61}[0-9A-Za-z])?(?:\.[0-9A-Za-z]([0-9A-Za-z-]{0,61}[0-9A-Za-z])?)*\.?$"
    if not re.match(hostname_regex, value):
        raise typer.BadParameter("Invalid hostname format")
    return value


env_template = """
# PostgreSQL Configuration
POSTGRES_DB=micado                # The name of the PostgreSQL database
POSTGRES_USER=micado              # The PostgreSQL database user
POSTGRES_PORT=5432
POSTGRES_PASSWORD={{ postgres_password }} # The password for the PostgreSQL database user

# Keycloak Configuration
KEYCLOAK_IMAGE_TAG=23.0.0         # The Docker image tag for the Keycloak image
KEYCLOAK_DB_USER=keycloak  # The database user for Keycloak
KEYCLOAK_DB_SCHEMA=keycloak         # The database schema for Keycloak
KEYCLOAK_DB_PWD={{ postgres_password }}                  # CHANGE IT
KC_LOG_LEVEL=INFO                 # The log level for Keycloak
KEYCLOAK_ADMIN=admin              # The admin username for Keycloak
KEYCLOAK_ADMIN_PASSWORD={{ keycloak_admin_password }} # The admin password for Keycloak
MICADO_KC_REALM_ADMIN_PASSWORD={{ keycloak_admin_password }}      # 
NGO_REALM_CLIENT_SECRET=secret               # CHANGE IT
MIGRANT_REALM_CLIENT_SECRET=secret           # CHANGE IT
PA_REALM_CLIENT_SECRET=secret                # CHANGE IT
IDENTITY_HOSTNAME={{ identity_hostname }} # The hostname for the Keycloak identity server
MIGRANTS_HOSTNAME={{ migrants_hostname }} # The hostname for the Migrants application
PA_HOSTNAME={{ pa_hostname }}       # The hostname for the Public Administration application
NGO_HOSTNAME={{ ngo_hostname }}     # The hostname for the NGO application

# Nginx Configuration
NGINX_IMAGE_TAG=1.25.3.1-3-buster-fat            # The Docker image tag for the Nginx image
MIGRANTS_IMAGE_TAG=v2.5.0
PA_IMAGE_TAG=v2.5.0
NGO_IMAGE_TAG=v2.5.0
BACKEND_IMAGE_TAG=v2.5.0

# Traefik Configuration
TRAEFIK_IMAGE_TAG=v2.11.2          # The Docker image tag for the Traefik image
TRAEFIK_LOG_LEVEL=DEBUG           # The log level for Traefik
TRAEFIK_ACME_EMAIL={{ traefik_acme_email }} # The email used for ACME certificate registration
TRAEFIK_HOSTNAME={{ traefik_hostname }} # The hostname for the Traefik dashboard

# Git Configuration
GIT_HOSTNAME={{ git_hostname }}     # The hostname for the Gitea Git server
GITEA_IMAGE_TAG=1.21.11            # The Docker image tag for the Gitea image
GITEA_DB_USER=gitea                # The database user for Gitea
GITEA_DB_PWD={{ gitea_db_password }}       # The password for the Gitea database user
GITEA_DB_SCHEMA=gitea               # The database schema for Gitea

# Weblate Configuration
WEBLATE_IMAGE_TAG=5.5.0.1          # The Docker image tag for the Weblate image
WEBLATE_EMAIL_HOST={{ weblate_email_host }} # The email host for Weblate
WEBLATE_EMAIL_HOST_USER={{ weblate_email_host_user }} # The email host user for Weblate
WEBLATE_SERVER_EMAIL={{ weblate_server_email }} # The server email for Weblate
WEBLATE_DEFAULT_FROM_EMAIL={{ weblate_default_from_email }} # The default from email for Weblate
WEBLATE_ALLOWED_HOSTS=*           # Allowed hosts for Weblate
WEBLATE_ADMIN_PASSWORD={{ weblate_admin_password }} # The admin password for Weblate
WEBLATE_ADMIN_NAME=admin          # The admin name for Weblate
WEBLATE_ADMIN_EMAIL={{ weblate_admin_email }} # The admin email for Weblate
TRANSLATION_HOSTNAME={{ translation_hostname }} # The hostname for the translation platform
WEBLATE_REGISTRATION_OPEN=true    # Whether registration is open on Weblate
WEBLATE_DB_SCHEMA=weblate
WEBLATE_POSTGRES_PASSWORD={{ weblate_postgres_password }} # The password for the Weblate PostgreSQL user
WEBLATE_POSTGRES_USER=weblate # The Weblate PostgreSQL user
WEBLATE_POSTGRES_HOST=micado_db   # The PostgreSQL host for Weblate
WEBLATE_POSTGRES_PORT=5432        # The PostgreSQL port for Weblate
WEBLATE_WORKERS=2                 # The number of worker processes for Weblate
TZ={{ timezone }}                  # The timezone for Weblate

# Redis Configuration
REDIS_IMAGE_TAG=7-alpine            # The Docker image tag for the Redis image

# Backend Configuration
MICADO_BACKEND_IMAGE_TAG=v2.5.0   # The Docker image tag for the backend image
MICADO_GIT_URL=http://git # The Git URL for the MICADO backend
MICADO_TRANSLATIONS_DIR=/translations # The directory for translations in the MICADO backend
MICADO_DB_PWD={{ micado_db_password }}  # The password for the MICADO database user
MICADO_DB_USER=micadoapp     # The MICADO database user
MICADO_DB_SCHEMA=micadoapp           # The database schema for the MICADO database
MICADO_ENV=prod            # The environment for the MICADO backend
MICADO_WEBLATE_PROJECT=micado
WEBLATE_EMAIL_HOST_SSL=true       # Whether to use SSL for the Weblate email host
WEBLATE_EMAIL_HOST_PASSWORD={{ weblate_email_host_password }} # The password for the Weblate email host user
ALGORITHM=aes-192-cbc                   # The algorithm used for security
SALT={{ algorithm_password }}                   # The salt value used for hashing
KEY_LENGTH=24                     # The key length for security
BUFFER_0=16           # Buffer value 0
BUFFER_1=0           # Buffer value 1
MICADO_WEBLATE_KEY={{ micado_weblate_key }}    # The key for Weblate integration
ALGORITHM_PASSWORD={{ algorithm_password }}                   # The salt value used for hashing

# Portainer Configuration
PORTAINER_IMAGE_TAG=2.19.5-alpine        # The Docker image tag for the Portainer image
PORTAINER_HOSTNAME={{ portainer_hostname }} # The hostname for the Portainer dashboard

TITLE_LIMIT=30

# --------- HOSTNAMES -----------
API_HOSTNAME={{ api_hostname }}          # backend API hostname


# -------- WEBLATE PART ----------
WEBLATE_DEBUG=0
WEBLATE_SITE_TITLE=MICADO weblate

"""

app = typer.Typer()


@app.command()
def environment(
    postgres_password: Annotated[
        str,
        typer.Option(
            prompt="Enter the PostgreSQL password",
            callback=pwd_callback,
            hide_input=True,
        ),
    ],
    keycloak_admin_password: Annotated[
        str,
        typer.Option(
            prompt="Enter the Keycloak admin password",
            callback=pwd_callback,
            hide_input=True,
        ),
    ],
    identity_hostname: Annotated[
        str,
        typer.Option(
            prompt="Enter the Keycloak identity hostname", callback=hostname_callback
        ),
    ],
    migrants_hostname: Annotated[
        str,
        typer.Option(
            prompt="Enter the Migrants application hostname", callback=hostname_callback
        ),
    ],
    pa_hostname: Annotated[
        str,
        typer.Option(
            prompt="Enter the Public Administration application hostname",
            callback=hostname_callback,
        ),
    ],
    ngo_hostname: Annotated[
        str,
        typer.Option(
            prompt="Enter the NGO application hostname", callback=hostname_callback
        ),
    ],
    traefik_acme_email: Annotated[
        str,
        typer.Option(prompt="Enter the Traefik ACME email", callback=email_callback),
    ],
    traefik_hostname: Annotated[
        str,
        typer.Option(prompt="Enter the Traefik hostname", callback=hostname_callback),
    ],
    git_hostname: Annotated[
        str,
        typer.Option(
            prompt="Enter the Gitea Git server hostname", callback=hostname_callback
        ),
    ],
    gitea_db_password: Annotated[
        str,
        typer.Option(
            prompt="Enter the Gitea database password",
            callback=pwd_callback,
            hide_input=True,
        ),
    ],
    weblate_email_host: Annotated[
        str,
        typer.Option(prompt="Enter the Weblate email host", callback=hostname_callback),
    ],
    weblate_email_host_user: Annotated[
        str, typer.Option(prompt="Enter the Weblate email host user")
    ],
    weblate_server_email: Annotated[
        str,
        typer.Option(prompt="Enter the Weblate server email", callback=email_callback),
    ],
    weblate_default_from_email: Annotated[
        str,
        typer.Option(
            prompt="Enter the Weblate default from email", callback=email_callback
        ),
    ],
    weblate_admin_password: Annotated[
        str,
        typer.Option(
            prompt="Enter the Weblate admin password",
            callback=pwd_callback,
            hide_input=True,
        ),
    ],
    weblate_admin_email: Annotated[
        str,
        typer.Option(prompt="Enter the Weblate admin email", callback=email_callback),
    ],
    translation_hostname: Annotated[
        str,
        typer.Option(
            prompt="Enter the Translation platform hostname", callback=hostname_callback
        ),
    ],
    weblate_postgres_password: Annotated[
        str,
        typer.Option(
            prompt="Enter the Weblate PostgreSQL password",
            callback=pwd_callback,
            hide_input=True,
        ),
    ],
    timezone: Annotated[str, typer.Option(prompt="Enter the timezone")],
    micado_db_password: Annotated[
        str,
        typer.Option(
            prompt="Enter the MICADO database password",
            callback=pwd_callback,
            hide_input=True,
        ),
    ],
    weblate_email_host_password: Annotated[
        str,
        typer.Option(
            prompt="Enter the Weblate email host password",
            callback=pwd_callback,
            hide_input=True,
        ),
    ],
    algorithm_password: Annotated[
        str,
        typer.Option(
            prompt="Enter the algorithm password",
            callback=pwd_callback,
            hide_input=True,
        ),
    ],
    micado_weblate_key: Annotated[
        str, typer.Option(prompt="Enter the MICADO Weblate key")
    ],
    portainer_hostname: Annotated[
        str,
        typer.Option(prompt="Enter the Portainer hostname", callback=hostname_callback),
    ],
    api_hostname: Annotated[
        str,
        typer.Option(prompt="Enter the API hostname", callback=hostname_callback),
    ],
):
    """
    Configures the MICADO application by prompting the user for various environment variables and then creating the necessary folders.

    The function takes several parameters that represent different environment variables needed for the MICADO application, such as database passwords, hostnames, and email settings. It then creates a dictionary of these environment variables and passes it to the `configure_env` function to update the application's configuration.

    Finally, the function creates a list of folders that are needed for the application and calls the `create_folder` function for each one.
    """
    print("Configuring MICADO application")
    print(f"You chose for the PostgreSQL password: {postgres_password}")
    print(f"You chose for the Keycloak admin password: {keycloak_admin_password}")
    print(f"You chose for the Keycloak identity hostname: {identity_hostname}")
    print(f"You chose for the Migrants application hostname: {migrants_hostname}")
    print(f"You chose for the Public Administration application hostname: {pa_hostname}")
    print(f"You chose for the NGO application hostname: {ngo_hostname}")
    print(f"You chose for the Traefik ACME email: {traefik_acme_email}")
    print(f"You chose for the Traefik hostname: {traefik_hostname}")
    print(f"You chose for the Gitea Git server hostname: {git_hostname}")
    print(f"You chose for the Gitea database password: {gitea_db_password}")
    print(f"You chose for the Weblate email host: {weblate_email_host}")
    print(f"You chose for the Weblate email host user: {weblate_email_host_user}")
    print(f"You chose for the Weblate server email: {weblate_server_email}")
    print(f"You chose for the Weblate default from email: {weblate_default_from_email}")
    print(f"You chose for the Weblate admin password: {weblate_admin_password}")
    print(f"You chose for the Weblate admin email: {weblate_admin_email}")
    print(f"You chose for the Translation platform hostname: {translation_hostname}")
    print(f"You chose for the Weblate PostgreSQL password: {weblate_postgres_password}")
    print(f"You chose for the timezone: {timezone}")
    print(f"You chose for the MICADO database password: {micado_db_password}")
    print(f"You chose for the Weblate email host password: {weblate_email_host_password}")
    print(f"You chose for the algorithm password: {algorithm_password}")
    print(f"You chose for the MICADO Weblate key: {micado_weblate_key}")
    print(f"You chose for the Portainer hostname: {portainer_hostname}")
    print(f"You chose for the API hostname: {api_hostname}")
    

    if not checks.check_prepared():
        print(
            "MICADO is not prepared, you must execute the [bold green]prepare[/bold green] command first"
        )
        return

    env_vars = {
        "postgres_password": postgres_password,
        "keycloak_admin_password": keycloak_admin_password,
        "identity_hostname": identity_hostname,
        "migrants_hostname": migrants_hostname,
        "pa_hostname": pa_hostname,
        "ngo_hostname": ngo_hostname,
        "traefik_acme_email": traefik_acme_email,
        "traefik_hostname": traefik_hostname,
        "git_hostname": git_hostname,
        "gitea_db_password": gitea_db_password,
        "weblate_email_host": weblate_email_host,
        "weblate_email_host_user": weblate_email_host_user,
        "weblate_server_email": weblate_server_email,
        "weblate_default_from_email": weblate_default_from_email,
        "weblate_admin_password": weblate_admin_password,
        "weblate_admin_email": weblate_admin_email,
        "translation_hostname": translation_hostname,
        "weblate_postgres_password": weblate_postgres_password,
        "timezone": timezone,
        "micado_db_password": micado_db_password,
        "weblate_email_host_password": weblate_email_host_password,
        "algorithm_password": algorithm_password,
        "micado_weblate_key": micado_weblate_key,
        "portainer_hostname": portainer_hostname,
        "api_hostname": api_hostname,
    }

    configure_env(env_template, env_vars)

    # this folder list is done like this because there is the need to have empty folder and the ZIP file, being generated from git repository, does not have them
    folder_list = [
        "db_data",
        "weblate_data",
        "redis_data",
        "shared_images",
        "translations_dir",
    ]
    [create_folder(i) for i in folder_list]


