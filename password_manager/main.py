#! /Users/Heorhi_Parkhomenka/code/python-password-manager/env/bin/python
from dotenv import load_dotenv
import pathlib
import os
import logging


if os.path.islink(__file__):
    real_path = os.path.realpath(__file__)
else:
    real_path = __file__
BASE_DIR = pathlib.Path(real_path).parent.parent.absolute()
CONFIG_NAME = "credentials.ini"
CONFIG_PATH = os.path.join(BASE_DIR, CONFIG_NAME)


def configure_logging():
    logfile_path = os.environ.get(
        "LOGFILE_PATH",
        BASE_DIR / "log.txt",
    )
    handler = logging.FileHandler(
        filename=logfile_path,
    )
    logging.basicConfig(
        format="%(asctime)s %(filename)s %(levelname)s:%(message)s",
        level=logging.INFO,
        handlers=[handler],
    )


def load_environment() -> None:
    """Loading environments variables from .env file."""
    env_path = os.path.join(BASE_DIR, ".env")
    load_dotenv(env_path)


def main():
    from cli.cli import app
    app()


if __name__ == "__main__":
    load_environment()
    configure_logging()
    main()
