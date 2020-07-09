import typing
from collections import namedtuple

from password_manager.security.security import hash_value, verify_value, decrypt_value
from password_manager.db.db import (
    add_account,
    find_account_by_login,
    add_bunch, Account,
    find_bunches_by_name,
    find_bunches_by_account_id,
    delete_bunches_by_ids,
)

BunchObject = namedtuple('BunchObject', ['id', 'login', 'password', 'name', 'account_id'])


class BunchService:
    @staticmethod
    def create_bunch(encrypted_login: str, encrypted_password: str, name: str, account: Account):
        add_bunch(encrypted_login, encrypted_password, name, account)

    @staticmethod
    def find_bunch(name: str, account: Account, key: bytes) -> typing.List[BunchObject]:
        bunches = find_bunches_by_name(name, account.id)
        decrypted_bunches = [
            BunchObject(
                bunch.id,
                decrypt_value(bunch.login, key),
                decrypt_value(bunch.password, key),
                bunch.name,
                bunch.account_id,
            )
            for bunch in bunches
        ]
        return decrypted_bunches

    @staticmethod
    def show_all_bunches(account: Account, key: bytes) -> typing.List[BunchObject]:
        bunches = find_bunches_by_account_id(account.id)
        decrypted_bunches = [
            BunchObject(
                bunch.id,
                decrypt_value(bunch.login, key),
                decrypt_value(bunch.password, key),
                bunch.name,
                bunch.account_id,
            )
            for bunch in bunches
        ]
        return decrypted_bunches

    @staticmethod
    def delete_bunches_by_ids(bunches: typing.List[int]) -> None:
        delete_bunches_by_ids(bunches)


class AccountService:
    @staticmethod
    def create_account(login: str, password: str) -> None:
        hashed_password = hash_value(password)
        try:
            add_account(login, hashed_password)
        except Exception as e:
            print(e)
        else:
            print("Account %s was added" % login)

    @staticmethod
    def identify_account(login: str, password: str) -> bool:
        account = find_account_by_login(login)
        return verify_value(account.password, password)

    @staticmethod
    def find_account(login: str) -> Account:
        return find_account_by_login(login)
