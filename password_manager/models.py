import os

from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
DB_PATH = os.environ.get('DB_PATH', 'sqlite:////./default_db.db')
engine = create_engine(DB_PATH)

Session = sessionmaker(bind=engine)


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    bunches = relationship('Bunch', backref='account')

    def __repr__(self):
        return f"<Account(username={self.username}, password={self.password})>"


class Bunch(Base):
    __tablename__ = 'bunches'

    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.id'))

    def __repr__(self):
        return f"<Bunch(login={self.login}, password={self.password}, name={self.name})"


Base.metadata.create_all(engine)
