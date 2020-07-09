import os
import typing

from password_manager.db.db_management import AccountService, BunchService
from password_manager.security.security import get_key, encrypt_value
from password_manager.db.db import close_connection


def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


class Menu:
    def __init__(self, account_service: AccountService):
        self._running = True
        self._account = None
        self._key = None
        self._account_service = account_service
        self._bunch_service = BunchService()

    def run(self, login: str) -> None:
        self._account = self._account_service.find_account(login)
        self._key = get_key(self._account.password)
        choices = {
            1: self._show_bunches,
            2: self._create_bunch,
            3: self._delete_bunch,
            4: self._find_bunch,
            0: self._exit
        }
        while self._running:
            self._draw_menu(login)
            choice = int(input(">>> "))
            choices.get(choice)()

    @staticmethod
    def _draw_menu(login: str) -> None:
        print("Welcome", login)
        print('1. Show bunches')
        print('2. Create bunch')
        print('3. Delete bunch')
        print('4. Find bunch')
        print('0. Exit')

    def _show_bunches(self) -> None:
        clear()
        bunches = self._bunch_service.show_all_bunches(self._account, self._key)
        if not bunches:
            self._print_message("No brunches yet")
            return
        output = [
            f"{i + 1}.Login: {bunch.login} | Password: {bunch.password} | {bunch.name}"
            for i, bunch in enumerate(bunches)
        ]
        self._print_message(output)

    def _create_bunch(self) -> None:
        run = True
        while run:
            clear()
            login = input('Login: ')
            password = input('Password: ')
            name = input('Name: ')
            clear()
            self._print_message("Login: %s | Password: %s | Name: %s" % (login, password, name))
            answer = input("Is data correct?[y/n]: ")
            if answer.lower() == "y":
                self._bunch_service.create_bunch(
                    encrypt_value(login, self._key),
                    encrypt_value(password, self._key),
                    name,
                    self._account,
                )
            run = False

    def _delete_bunch(self) -> None:
        clear()
        run = True
        bunches = self._bunch_service.show_all_bunches(self._account, self._key)
        if not bunches:
            self._print_message("No bunches to delete")
            return
        while run:
            try:
                self._show_bunches()
                indexes = input("Enter indexes of bunches you want to delete: ")
                indexes = [int(index) - 1 for index in indexes.split()]
                bunches = self._bunch_service.show_all_bunches(self._account, self._key)
                bunch_ids = [bunch.id for i, bunch in enumerate(bunches) if i in indexes]
                answer = input("Are you sure you want to delete bunches?[y/n]")
                if answer == "y":
                    self._bunch_service.delete_bunches_by_ids(bunch_ids)
                run = False
            except ValueError:  # If type of one index is not int it will raise error
                self._print_message('Indexes can be only numbers')
        clear()

    def _find_bunch(self) -> None:
        clear()
        name = input("Enter the name: ")
        bunches = self._bunch_service.find_bunch(name, self._account, self._key)
        if not bunches:
            self._print_message("No brunches with such name: %s" % name)
            return
        output = [f"Login: {bunch.login} | Password: {bunch.password} | {bunch.name}" for bunch in bunches]
        self._print_message(output)

    def _exit(self) -> None:
        self._running = False
        close_connection()
        print("Exiting...")

    @staticmethod
    def _print_message(output: typing.Union[typing.List[str], str]) -> None:
        if isinstance(output, list):
            delimiter = "=" * len(max(output, key=lambda i: len(i)))
            print(delimiter)
            print("\n".join(output))
            print(delimiter)
        else:
            delimiter = "=" * len(output)
            print(delimiter)
            print(output)
            print(delimiter)
