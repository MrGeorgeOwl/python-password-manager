from password_manager.db.db_management import AccountService, BunchService
from password_manager.security.security import get_key, encrypt_value
from password_manager.db.db import close_connection


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

    def _show_bunches(self):
        bunches = self._bunch_service.show_all_bunches(self._account, self._key)
        if not bunches:
            print("No brunches yet")
            return
        output = [
            f"{i + 1}.Login: {bunch.login} | Password: {bunch.password} | {bunch.name}"
            for i, bunch in enumerate(bunches)
        ]
        delimiter = "=" * len(max(output, key=lambda i: len(i)))
        print(delimiter)
        print("\n".join(output))
        print(delimiter)

    def _create_bunch(self):
        login = input('Login: ')
        password = input('Password: ')
        name = input('Name: ')
        self._bunch_service.create_bunch(
            encrypt_value(login, self._key), 
            encrypt_value(password, self._key), 
            name, 
            self._account,
        )

    def _delete_bunch(self):
        # TODO: Implement check input of user
        self._show_bunches()
        indexes = input("Enter indexes of bunches you want to delete: ")
        indexes = [int(index) - 1 for index in indexes.split()]
        bunches = self._bunch_service.show_all_bunches(self._account, self._key)
        bunch_ids = [bunch.id for i, bunch in enumerate(bunches) if i in indexes]
        self._bunch_service.delete_bunches_by_ids(bunch_ids)

    def _find_bunch(self):
        name = input("Enter the name: ")
        bunches = self._bunch_service.find_bunch(name, self._account, self._key)
        if not bunches:
            print("No brunches with such name: %s" % name)
            return
        output = [f"Login: {bunch.login} | Password: {bunch.password} | {bunch.name}" for bunch in bunches]
        delimiter = "=" * len(output[0])
        print(delimiter)
        print("\n".join(output))
        print(delimiter)

    def _exit(self) -> None:
        self._running = False
        close_connection()
        print("Exiting...")
