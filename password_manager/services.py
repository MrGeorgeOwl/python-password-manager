from __future__ import annotations
from collections import namedtuple
import logging
import typing

from sqlalchemy import and_

from models import Session, Account, Bunch
from security import verify_value, hash_value, decrypt_value, encrypt_value

BunchObject = namedtuple('BunchObject', ['id', 'login', 'password', 'name', 'account_id'])


class OutputableException(BaseException):
    pass


class AccountService:
    def __init__(self, session: Session):
        self.session = session

    def find_account_by_username(self, username: str) -> typing.Optional[Account]:
        return self.session\
                .query(Account)\
                .filter_by(username=username)\
                .one_or_none()

    def add_account(self, username: str, password: str) -> None:
        hashed_password = hash_value(password)
        self.session.add(
            Account(
                username=username,
                password=hashed_password,
            ),
        )
        self.session.commit()

    def identify_account(self, username: str, password: str) -> bool:
        logging.info("Finding account by login: %s" % username)
        account = self.find_account_by_username(username)
        if not account:
            return False
        return verify_value(account.password, password)

    def authorize_user(
        self, 
        username: str, 
        password: str,
    ) -> typing.Optional[Account]:
        if self.identify_account(username, password):
            return self.find_account_by_username(username)
        return None


class BunchService:
    def __init__(self, session: Session, key: bytes):
        self.session = session
        self._key = key

    def add_bunch(
        self,
        username: str,
        password: str,
        name: str,
        account: Account,
    ) -> None:
        """Encrypt bunch info by key of current user and add it to db."""
        encrypted_username = encrypt_value(username, self._key)
        encrypted_password = encrypt_value(password, self._key)
        account.bunches.append(
            Bunch(
                login=encrypted_username,
                password=encrypted_password,
                name=name,
                account_id=account.id,
            ),
        )
        logging.info(f"Added new bunch for account: {account}")
        self.session.commit()

    def _find_bunches_by_name(self, name: str, account_id: int) -> typing.List[Bunch]:
        """Find bunches by name of the bunch."""
        return self.session.query(Bunch).filter(
            and_(
                Bunch.name.ilike(f'%{name}%'),
                Bunch.account_id == account_id,
            )
        )

    def find_bunches_by_account_id(self, account_id: int) -> typing.List[Bunch]:
        return self.session\
                .query(Bunch)\
                .filter_by(account_id=account_id)

    def delete_bunches_by_ids(self, bunch_ids: typing.List[int]) -> None:
        """Delete bunches with provided ids."""
        self.session\
            .query(Bunch)\
            .filter(Bunch.id.in_(bunch_ids))\
            .delete(synchronize_session="fetch")
        self.session.commit()

    def get_all_bunches(self, account: Account) -> typing.List[BunchObject]:
        """Return list of Bunch object and decrypt them with provided key."""
        logging.info("Finding bunches by account_id: %d" % account.id)
        bunches = self.find_bunches_by_account_id(account.id)
        decrypted_bunches = [
            BunchObject(
                bunch.id,
                decrypt_value(bunch.login, self._key),
                decrypt_value(bunch.password, self._key),
                bunch.name,
                bunch.account_id,
            )
            for bunch in bunches
        ]
        return decrypted_bunches

    def find_bunch(self, name: str, account: Account) -> typing.Optional[BunchObject]:
        """Find bunches if they exists and decrypt them with provided key."""
        logging.info("Finding bunches with name: %s" % name)
        bunches = self._find_bunches_by_name(name, account.id)
        decrypted_bunches = [
            BunchObject(
                bunch.id,
                decrypt_value(bunch.login, self._key),
                decrypt_value(bunch.password, self._key),
                bunch.name,
                bunch.account_id,
            )
            for bunch in bunches
        ]
        return decrypted_bunches[0] if decrypted_bunches else None

    def delete_bunch_by_name(self, name: str, account: Account) -> None:
        bunches = self._find_bunches_by_name(name, account.id)
        if not bunches:
            raise OutputableException(f"No bunch named {name}")
        self.session.query(Bunch).filter(
            Bunch.id == bunches[0].id,
        ).delete(synchronize_session="fetch")
        self.session.commit()
