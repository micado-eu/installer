import os

def check_prepared() -> bool:
    """
    Check if the necessary files and directories are present in the working directory.
    
    Returns:
    bool: True if all required files and directories are present, False otherwise.
    """
    required_files = ["docker-compose.yaml"]
    required_dirs = ["db_init", "keycloak", "nginx"]
    
    all_present = True
    
    for file in required_files:
        if not os.path.isfile(file):
            print(f"Required file missing: {file}")
            all_present = False
    
    for directory in required_dirs:
        if not os.path.isdir(directory):
            print(f"Required directory missing: {directory}")
            all_present = False
    
    if all_present:
        print("All required files and directories are present. The environment is prepared.")
        return True
    else:
        return False

def check_configured() -> bool:
    """
    Validate the .env file created by config.py to ensure all expected environment variables are present.
    
    Returns:
    bool: True if all required environment variables are present, False otherwise.
    """
    required_env_vars = [
        "POSTGRES_PASSWORD",
        "KEYCLOAK_ADMIN_PASSWORD",
        "IDENTITY_HOSTNAME",
        "MIGRANTS_HOSTNAME",
        "PA_HOSTNAME",
        "NGO_HOSTNAME",
        "ANALYTIC_HOSTNAME",
        "TRAEFIK_ACME_EMAIL",
        "TRAEFIK_HOSTNAME",
        "GIT_HOSTNAME",
        "GITEA_DB_PASSWORD",
        "WEBLATE_EMAIL_HOST",
        "WEBLATE_EMAIL_HOST_USER",
        "WEBLATE_SERVER_EMAIL",
        "WEBLATE_DEFAULT_FROM_EMAIL",
        "WEBLATE_ADMIN_PASSWORD",
        "WEBLATE_ADMIN_EMAIL",
        "TRANSLATION_HOSTNAME",
        "WEBLATE_POSTGRES_PASSWORD",
        "TZ",
        "ROCKETCHAT_HOSTNAME",
        "ROCKETCHAT_ADMIN_PASSWORD",
        "COUNTLY_MIGRANTS_APP_ID",
        "COUNTLY_MIGRANTS_API_KEY",
        "MICADO_DB_PASSWORD",
        "WEBLATE_EMAIL_HOST_PASSWORD",
        "COUNTLY_ADMIN_PASSWORD",
        "ALGORITHM_PASSWORD",
        "MICADO_WEBLATE_KEY",
        "PORTAINER_HOSTNAME",
    ]
    
    if not os.path.isfile(".env"):
        print("The .env file is missing.")
        return False

    with open(".env", "r") as f:
        env_content = f.read()

    all_present = True

    for var in required_env_vars:
        if f"{var}=" not in env_content:
            print(f"Required environment variable missing: {var}")
            all_present = False

    if all_present:
        print("All required environment variables are present. The environment is configured.")
        return True
    else:
        return False
