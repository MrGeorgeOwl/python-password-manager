#!/Users/georgy.parhomenko/code/PythonProjects/password_manager/env/bin/python
from dotenv import load_dotenv
import pathlib
import os
import logging


BASE_DIR = pathlib.Path(__file__).parent.parent.absolute()
CONFIG_NAME = "credentials.ini"
CONFIG_PATH = os.path.join(BASE_DIR, CONFIG_NAME)


def configure_logging():
    handler = logging.FileHandler(
        filename=os.environ.get("LOGFILE_PATH"),
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
