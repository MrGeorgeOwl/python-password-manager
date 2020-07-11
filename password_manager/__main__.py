from dotenv import load_dotenv
import pathlib
import os
import logging


def load_environment() -> None:
    """Loading environments variables from .env file."""
    env_path = os.path.join(pathlib.Path(__file__).parent.absolute(), ".env")
    load_dotenv(env_path)


def main():
    load_environment()
    logging.basicConfig(
        filename=os.environ.get("LOGFILE_PATH"),
        filemode='w',
        format="%(asctime)s %(levelname)s:%(message)s",
        level=logging.DEBUG,
    )
    logger = logging.getLogger(__name__)

    from password_manager.menu.menu import Menu
    from password_manager.db.db_management import AccountService
    logger.info("Reading user input")
    login = input("Enter login: ")
    password = input("Enter password: ")
    account_service = AccountService()
    menu = Menu(account_service)
    logging.info("Verifying user: %s" % login)
    if not account_service.identify_account(login, password):
        print("Access denied")
        return
    menu.run(login)


if __name__ == "__main__":
    main()
