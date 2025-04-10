from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from models import Model

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

class Model(Base):
    __tablename__ = 'models'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description}
