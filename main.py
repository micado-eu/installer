import typer

import app.commands.prepare as prepare
import app.commands.configure as configure
import app.commands.deploy as deploy

app = typer.Typer()

app.add_typer(prepare.app, name="prepare")
app.add_typer(configure.app, name="configure")
app.add_typer(deploy.app, name="deploy")

if __name__ == "__main__":
    app()
