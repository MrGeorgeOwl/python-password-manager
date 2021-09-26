from __future__ import annotations
import configparser
import os
import typing
from functools import wraps
from typing import List

import typer

from models import Session
from main import CONFIG_PATH
from security.security import get_key
from services import AccountService

if typing.TYPE_CHECKING:
    from services import BunchObject


def authenticated(f):
    @wraps(f)
    def wrapper(ctx: typer.Context, *args, **kwargs):
        if not _is_config_exists():
            typer.echo('First you should log in.\nType "login" command')
            return
        session = ctx.meta['session']
        config = get_config()
        username, password = config['default']['username'], config['default']['password']
        service = AccountService(session)
        if not (user := service.authorize_user(username, password)):
            typer.echo("Wrong credentials.")
            raise typer.Exit()
        ctx.meta['user'] = user
        ctx.meta['key'] = get_key(user.password)
        f(ctx, *args, **kwargs)
    return wrapper


def _is_config_exists() -> bool:
    return os.path.exists(CONFIG_PATH)


def get_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    return config


def db_session(f):
    @wraps(f)
    def wrapper(ctx: typer.Context, *args, **kwargs):
        with Session() as session:
            ctx.meta['session'] = session
            return f(ctx, *args, **kwargs)
    return wrapper


def prepare_bunches_for_output(bunches: List[BunchObject]) -> str:
    output = [
        f'{bunch.login} {bunch.password} {bunch.name}'
        for bunch in bunches
    ]
    output = ["Login Password Name"] + output[:]
    return "\n".join(output)
