import configparser
import logging

import typer
import pyperclip

from cli.helpers import authenticated, db_session, prepare_bunches_for_output
from main import CONFIG_PATH
from services import BunchService, OutputableException

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
@db_session
@authenticated
def show_bunches(ctx: typer.Context) -> None:
    """List bunches available for current user."""
    try:
        service = BunchService(ctx.meta['session'], ctx.meta['key'])
        bunches = service.get_all_bunches(ctx.meta['user'])
        output = prepare_bunches_for_output(bunches)
        typer.echo(output)
    except Exception as e:
        typer.echo(f"Something went wrong. Check log file.")
        logging.error(e)


@app.command()
@db_session
@authenticated
def search(ctx: typer.Context, name: str) -> None:
    service = BunchService(ctx.meta['session'], ctx.meta['key'])
    try:
        bunch = service.find_bunch(name, ctx.meta['user'])
        if not bunch:
            typer.echo(f"No bunch named {name}")
            raise typer.Exit()
        output = prepare_bunches_for_output([bunch])
        typer.echo(output)
    except RuntimeError:
        pass
    except Exception as e:
        typer.echo(f"Something went wrong. Check log file.")
        logging.error(e)


@app.command()
@db_session
@authenticated
def copy(ctx: typer.Context, name: str) -> None:
    service = BunchService(ctx.meta['session'], ctx.meta['key'])
    try:
        bunch = service.find_bunch(name, ctx.meta['user'])
        if not bunch:
            typer.echo(f"No bunch named: {name}")
            raise typer.Exit()
        copying_value = f"{bunch.login}\n{bunch.password}"
        pyperclip.copy(copying_value)
        typer.echo("Copied bunch info to clipboard.")
    except Exception as e:
        typer.echo(f"Something went wrong. Check log file.")
        logging.error(e)


@app.command()
@db_session
@authenticated
def add(ctx: typer.Context, login: str, password: str, name: str) -> None:
    service = BunchService(ctx.meta['session'], ctx.meta['key'])
    try:
        service.add_bunch(login, password, name, ctx.meta['user'])
        typer.echo(f"Bunch for {name} was successfully added.")
    except Exception as e:
        typer.echo(f"Something went wrong. Check log file.")
        logging.error(e)


@app.command()
@db_session
@authenticated
def delete(ctx: typer.Context, name: str) -> None:
    service = BunchService(ctx.meta['session'], ctx.meta['key'])
    try:
        service.delete_bunch_by_name(name, ctx.meta['user'])
        typer.echo("Bunch was deleted.")
    except OutputableException as e:
        typer.echo(e)
    except Exception as e:
        typer.echo(f"Something went wrong. Check log file.")
        logging.error(e)
