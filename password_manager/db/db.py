import os
import typing

from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
DB_PASS = os.environ.get('DB_PASS')
engine = create_engine("postgresql+psycopg2://password_manager:%s@localhost:5432/password_manager" % DB_PASS)

Session = sessionmaker(bind=engine)


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

    def __repr__(self):
        return "<Account(username=%s, password=%s)>" % (self.username, self.password)


class Bunch(Base):
    __tablename__ = 'bunches'

    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.id'))

    account = relationship('Account', back_populates='bunches')

    def __repr__(self):
        return "<Bunch(login=%s, password=%s, name=%s)" % (self.login, self.password, self.name)


Account.bunches = relationship('Bunch', order_by=Bunch.id, back_populates='account')

session = Session()


def find_account_by_login(login: str) -> Account:
    account = session.query(Account).filter_by(username=login)[0]
    return account


def add_account(login: str, hashed_password: str) -> None:
    session.add(
        Account(username=login, password=hashed_password),
    )
    session.commit()


def add_bunch(encrypted_login: str, encrypted_password: str, name: str, account: Account):
    account.bunches.append(
        Bunch(login=encrypted_login, password=encrypted_password, name=name, account_id=account.id),
    )
    session.commit()


def find_bunches_by_name(name: str, account_id: int) -> typing.List[Bunch]:
    return session.query(Bunch).filter_by(name=name, account_id=account_id)


def find_bunches_by_account_id(account_id: int) -> typing.List[Bunch]:
    return session.query(Bunch).filter_by(account_id=account_id)


def delete_bunches_by_ids(bunch_ids: typing.List[int]) -> None:
    # TODO: Implement check if ids exist
    stmt = Bunch.__table__.delete().where(Bunch.id.in_(bunch_ids))
    engine.execute(stmt)


def close_connection() -> None:
    session.close()
