from dotenv import load_dotenv
import pathlib
import os


def load_environment() -> None:
    env_path = os.path.join(pathlib.Path(__file__).parent.absolute(), ".env")
    load_dotenv(env_path)


def main():
    load_environment()
    os.environ.get("DB_PASS")

    from password_manager.menu.menu import Menu
    from password_manager.db.db_management import AccountService
    # login = input("Enter login: ")
    # password = input("Enter password: ")
    account_service = AccountService()
    menu = Menu(account_service)
    login = 'George'
    password = '1o1CopyOf1Password'
    if not account_service.identify_account(login, password):
        print("Access denied")
        return
    menu.run(login)


if __name__ == "__main__":
    main()
