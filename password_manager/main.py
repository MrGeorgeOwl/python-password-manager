#!/Users/georgy.parhomenko/code/PythonProjects/password_manager/env/bin/python
from dotenv import load_dotenv
import pathlib
import os
import logging
import sys


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
    env_path = os.path.join(pathlib.Path(__file__).parent.parent.absolute(), ".env")
    load_dotenv(env_path)


def proccess_console_commands() -> None:
    try:
        command, new_login, new_password = sys.argv[1:]
        if command != "create":
            print("Sry I dont know that command yet :(")
        else:
            AccountService.create_account(new_login, new_password)
            print("Account was %s created" % new_login)
    except ValueError:
        print("Enter login and password of new account")


def main():
    from menu.menu import Menu
    logging.info("Reading user input")
    login = input("Enter login: ")
    password = input("Enter password: ")
    menu = Menu()
    logging.info("Verifying user: %s" % login)
    if not AccountService.identify_account(login, password):
        print("Access denied")
        return
    menu.run(login)


if __name__ == "__main__":
    load_environment()
    configure_logging()
    from db.db_management import AccountService
    if len(sys.argv) > 1:
        proccess_console_commands()
    else:
        main()
