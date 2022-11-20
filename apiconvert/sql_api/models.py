import datetime
from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False)
    password = Column(String(32), nullable=False)
    email = Column(String(256))

    def __repr__(self):
        return f"{self.username} - {self.email}"

class File(Base):
    __tablename__ = 'files'

    id        = Column(Integer, primary_key=True)
    fileName  = Column(String(128), nullable=False)
    newFormat = Column(String(128), nullable=False)
    oldFormat = Column(String(128))
    status    = Column(String(128), nullable=False, default='uploaded')
    timeStamp = Column(DateTime(), default=datetime.datetime.utcnow)
    pathName  = Column(String, nullable= False)
    user      = Column(Integer, ForeignKey('users.id'))
    
    def __repr__(self):
        return f"{self.fileName} - {self.newFormat} - {self.timeStamp} - {self.status}"