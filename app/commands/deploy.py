import typer
import subprocess
from rich import print
from app.core.checks import check_prepared
import shlex

app = typer.Typer()

@app.command()
def compose_up():
    """
    Deploy the MICADO application using docker-compose up.
    """
    if not check_prepared():
        print("[bold red]The environment is not prepared. Please ensure all necessary files and directories are present before deploying.[/bold red]")
        return

    print("Deploying MICADO application")
    try:
        result = subprocess.run(["docker", "compose", "up", "-d"], check=True)
        if result.returncode == 0:
            print("[bold green]MICADO application deployed successfully![/bold green]")
        else:
            print("[bold red]Failed to deploy MICADO application.[/bold red]")
    except subprocess.CalledProcessError as e:
        print(f"[bold red]Error occurred while deploying MICADO application: {e}[/bold red]")

@app.command()
def compose_down():
    """
    Stop and remove the MICADO application using docker-compose down.
    """
    print("Stopping and removing MICADO application")
    try:
        result = subprocess.run(["docker", "compose", "down"], check=True)
        if result.returncode == 0:
            print("[bold green]MICADO application stopped and removed successfully![/bold green]")
        else:
            print("[bold red]Failed to stop and remove MICADO application.[/bold red]")
    except subprocess.CalledProcessError as e:
        print(f"[bold red]Error occurred while stopping and removing MICADO application: {e}[/bold red]")


@app.command("finalize_deployment")
def finalize_deployment(
    env_file: Annotated[str, typer.Option(help="Path to .env file", default=".env")] = ".env",
):
    """
    Finalize the MiCADO deployment by creating the Gitea admin user
    inside the running container.
    """
    typer.echo("🔧 Finalizing deployment...")

    # Load env vars
    if not os.path.exists(env_file):
        typer.echo(f"❌ Cannot find environment file: {env_file}")
        raise typer.Exit(code=1)

    env_vars = get_env_vars(env_file)

    # Get required values
    username = env_vars.get("gitea_admin_username", "root")
    password = env_vars.get("gitea_admin_password")
    email = env_vars.get("gitea_admin_email")

    if not all([password, email]):
        typer.echo("❌ Missing Gitea admin credentials in .env file.")
        raise typer.Exit(code=1)

    typer.echo(f"🧩 Creating Gitea admin user {username} ({email}) ...")

    cmd = [
        "docker",
        "compose",
        "exec",
        "-it",
        "--user",
        "1000",
        "git",
        "gitea",
        "admin",
        "user",
        "create",
        "--username",
        username,
        "--password",
        password,
        "--email",
        email,
        "--admin",
    ]

    try:
        subprocess.run(cmd, check=True)
        typer.echo("✅ Gitea admin user created successfully!")
    except subprocess.CalledProcessError as e:
        typer.echo(f"❌ Failed to create Gitea admin user: {e}")
        raise typer.Exit(code=1)





if __name__ == "__main__":
    app()


