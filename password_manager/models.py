import os

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



Base.metadata.create_all(engine)
