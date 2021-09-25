import logging
import typing
from collections import namedtuple

from security.security import hash_value, verify_value, decrypt_value
from db.db import Account, AccountRepo, BunchRepo

logger = logging.getLogger(__name__)

BunchObject = namedtuple('BunchObject', ['id', 'login', 'password', 'name', 'account_id'])


class BunchService:
    @staticmethod
    def create_bunch(encrypted_login: str, encrypted_password: str,
                     name: str, account: Account) -> None:
        """Create bunch with given variables."""
        try:
            logger.info("Receive bunch for account: %s" % account)
            BunchRepo.add_bunch(encrypted_login, encrypted_password, name, account)
            logger.info("Added new bunch for account: %s" % account)
        except Exception as e:
            logger.warning(e)

    @staticmethod
    def find_bunch(name: str, account: Account, key: bytes) -> typing.List[BunchObject]:
        """Find bunches if they exists and decrypt them with provided key."""
        try:
            logging.info("Finding bunches with name: %s" % name)
            bunches = BunchRepo.find_bunches_by_name(name, account.id)
            logging.info("Decrypting bunches")
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
        except Exception as e:
            logger.warning(e)

    @staticmethod
    def get_all_bunches(account: Account, key: bytes) -> typing.List[BunchObject]:
        """Return list of Bunch object and decrypt them with provided key."""
        try:
            logger.info("Finding bunches by account_id: %d" % account.id)
            bunches = BunchRepo.find_bunches_by_account_id(account.id)
            logger.info("Decrypting bunches")
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
        except Exception as e:
            logger.warning(e)

    @staticmethod
    def delete_bunches_by_ids(bunches: typing.List[int]) -> None:
        """Delete bunches with provided ids."""
        try:
            logger.info("Deleting bunches with ids: ", bunches)
            BunchRepo.delete_bunches_by_ids(bunches)
        except Exception as e:
            logger.warning(e)


class AccountService:
    @staticmethod
    def create_account(login: str, password: str) -> None:
        """Hash login and password and add account to database."""
        hashed_password = hash_value(password)
        try:
            logging.info("Adding account\nLogin: %s\nPassword: %s" % (login, password))
            AccountRepo.add_account(login, hashed_password)
        except Exception as e:
            logger.warning(e)

    @staticmethod
    def identify_account(login: str, password: str) -> bool:
        try:
            logging.info("Finding account by login: %s" % login)
            account = AccountRepo.find_account_by_login(login)
            if not account:
                print("No such account: %s" % login)
                return False
            return verify_value(account.password, password)
        except Exception as e:
            logger.warning(e)

    @staticmethod
    def find_account(login: str) -> typing.Optional[Account]:
        try:
            logging.info("Finding account by login: %s" % login)
            return AccountRepo.find_account_by_login(login)
        except Exception as e:
            logger.warning(e)
