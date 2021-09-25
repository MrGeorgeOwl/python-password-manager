import configparser

import typer

from cli.helpers import authenticated
from main import CONFIG_PATH

app = typer.Typer()


@app.command()
def login(username: str, password: str):
    """Creates config file which will be used in future for user authentication."""
    config = configparser.ConfigParser()
    config['default'] = {
        "username": username,
        "password": password,
    }
    with open(CONFIG_PATH, 'w') as file:
        config.write(file)
    typer.echo(f"Credentials for {username} was successfully created!")


@app.command()
@authenticated
def hello(ctx: typer.Context) -> None:
    typer.echo(f"Hello, {ctx.meta['username']}")
