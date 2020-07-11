from dotenv import load_dotenv
import pathlib
import os
import logging
import sys


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
    logging.basicConfig(
        filename=os.environ.get("LOGFILE_PATH"),
        filemode='w',
        format="%(asctime)s %(filename)s %(levelname)s:%(message)s",
        level=logging.DEBUG,
    )
    logger = logging.getLogger(__name__)

    from password_manager.menu.menu import Menu
    logger.info("Reading user input")
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
    from password_manager.db.db_management import AccountService
    if len(sys.argv) > 1:
        proccess_console_commands()
    else:
        main()
