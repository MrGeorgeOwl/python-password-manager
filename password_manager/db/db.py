import os
import typing

from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
DB_PATH = os.environ.get('DB_PATH')
engine = create_engine("sqlite:////%s" % DB_PATH)

Session = sessionmaker(bind=engine)


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    bunches = relationship('Bunch', backref='account')

    def __repr__(self):
        return "<Account(username=%s, password=%s)>" % (self.username, self.password)


class Bunch(Base):
    __tablename__ = 'bunches'

    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.id'))

    def __repr__(self):
        return "<Bunch(login=%s, password=%s, name=%s)" % (self.login, self.password, self.name)


session = Session()


def find_account_by_login(login: str) -> typing.Optional[Account]:
    return session.query(Account).filter_by(username=login).one_or_none()


def add_account(login: str, hashed_password: str) -> None:
    session.add(
        Account(username=login, password=hashed_password),
    )
    session.commit()


def add_bunch(encrypted_login: str, encrypted_password: str, name: str, account: Account) -> None:
    account.bunches.append(
        Bunch(login=encrypted_login, password=encrypted_password, name=name, account_id=account.id),
    )
    session.commit()


def find_bunches_by_name(name: str, account_id: int) -> typing.List[Bunch]:
    return session.query(Bunch).filter_by(name=name, account_id=account_id)


def find_bunches_by_account_id(account_id: int) -> typing.List[Bunch]:
    return session.query(Bunch).filter_by(account_id=account_id)


def delete_bunches_by_ids(bunch_ids: typing.List[int]) -> None:
    stmt = Bunch.__table__.delete().where(Bunch.id.in_(bunch_ids))
    engine.execute(stmt)


def close_connection() -> None:
    session.close()


Base.metadata.create_all(engine)
