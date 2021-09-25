import configparser
import os
from functools import wraps

import typer

from main import CONFIG_PATH


def authenticated(func):
    @wraps(func)
    def wrapper(ctx: typer.Context, *args, **kwargs):
        if _is_config_exists():
            ctx.meta['username'] = _get_username()
            func(ctx, *args, **kwargs)
        else:
            typer.echo('First you should log in.\nType "login" command')
    return wrapper


def _is_config_exists() -> bool:
    return os.path.exists(CONFIG_PATH)


def _get_username() -> str:
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    return config['default']['username']
