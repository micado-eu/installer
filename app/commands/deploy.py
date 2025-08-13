import typer
import subprocess
from rich import print
from app.core.checks import check_prepared

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

if __name__ == "__main__":
    app()
