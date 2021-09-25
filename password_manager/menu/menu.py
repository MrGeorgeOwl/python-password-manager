import os
import typing
from collections import namedtuple

from db.db_management import AccountService, BunchService
from security.security import get_key
from db.db import close_connection


InputBunch = namedtuple('InputBunch', ['login', 'password', 'name'])


def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


class Menu:
    """Class for console menu."""
    def __init__(self):
        self._running = True
        self._account = None
        self._key = None

    def run(self, login: str) -> None:
        """Start menu."""
        clear()
        self._account = AccountService.find_account(login)
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
        """Draw menu with choices."""
        print("Welcome", login)
        print('1. Show bunches')
        print('2. Create bunch')
        print('3. Delete bunch')
        print('4. Find bunch')
        print('0. Exit')

    def _show_bunches(self) -> None:
        """Print bunches of authorized user."""
        clear()
        bunches = BunchService.get_all_bunches(self._account, self._key)
        if not bunches:
            self._print_message("No bunches yet")
            return
        output = [
            f"{i + 1}.Login: {bunch.login} | Password: {bunch.password} | {bunch.name}"
            for i, bunch in enumerate(bunches)
        ]
        self._print_message(output)

    def _create_bunch(self) -> None:
        """Accept user input and create new bunch from it."""
        run = True
        while run:
            clear()
            bunch = self._input_new_bunch()
            clear()
            self._print_message(
                "Login: %s | Password: %s | Name: %s"
                % (bunch.login, bunch.password, bunch.name)
            )
            if self._verify_new_bunch():
                BunchService.create_bunch(
                    bunch.login,
                    bunch.password,
                    bunch.name,
                    self._account,
                    self._key
                )
            clear()
            self._print_message("Bunch was created")
            run = False

    @staticmethod
    def _input_new_bunch() -> InputBunch:
        """Take input of user."""
        login = input('Login: ')
        password = input('Password: ')
        name = input('Name: ')
        return InputBunch(login, password, name)

    @staticmethod
    def _verify_new_bunch() -> bool:
        """Asks user if he write bunch correct."""
        answer = input("Is data correct?[y/n]: ")
        return answer.lower() == "y"

    def _delete_bunch(self) -> None:
        """Deleting bunches of inputted indexes."""
        clear()
        bunches = BunchService.get_all_bunches(self._account, self._key)
        if not bunches:
            self._print_message("No bunches to delete")
            return
        # Ask user about deleting brunch until he choose one
        try:
            self._show_bunches()
            bunch_ids = self._bunch_ids_from_input()
            answer = input("Are you sure you want to delete bunches?[y/n]")
            if answer == "y":
                BunchService.delete_bunches_by_ids(bunch_ids)
        except ValueError:  # If type of one index is not int it will raise error
            self._print_message('Indexes must be numbers')
        clear()
        self._print_message("Bunch(es) was deleted")

    def _bunch_ids_from_input(self) -> typing.List[int]:
        """Take indexes of bunches from input and get their ids."""
        indexes = input("Enter indexes of bunches you want to delete: ")
        indexes = [int(index) - 1 for index in indexes.split()]
        bunches = BunchService.get_all_bunches(self._account, self._key)
        return [bunch.id for i, bunch in enumerate(bunches) if i in indexes]

    def _find_bunch(self) -> None:
        """Look for bunch by inputted by user name."""
        clear()
        name = input("Enter the name of bunch: ")
        clear()
        bunches = BunchService.find_bunch(name, self._account, self._key)
        if not bunches:
            self._print_message("No brunches with such name: %s" % name)
            return
        output = [f"Login: {bunch.login} | Password: {bunch.password} | {bunch.name}" for bunch in bunches]
        self._print_message(output)

    def _exit(self) -> None:
        self._running = False
        close_connection()
        clear()
        print("Exiting...")

    @staticmethod
    def _print_message(output: typing.Union[typing.List[str], str]) -> None:
        """Output lists or one message in beautiful manner."""
        if isinstance(output, list):
            delimiter = "=" * len(max(output, key=lambda i: len(i)))
            output = "\n".join(output)
            print(f'{delimiter}\n{output}\n{delimiter}')
        else:
            delimiter = "=" * len(output)
            print(f'{delimiter}\n{output}\n{delimiter}')
