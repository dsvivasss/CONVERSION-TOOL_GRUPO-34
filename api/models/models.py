from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from .connection import session, get_engine, get_session
import datetime


Base    = declarative_base()
session = session

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False)
    password = Column(String(32), nullable=False)
    email = Column(String(256))

    def __repr__(self):
        return f"{self.username} - {self.email}"
    
class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True
    
class File(Base):
    __tablename__ = 'files'

    id        = Column(Integer, primary_key=True)
    fileName  = Column(String(128), nullable=False)
    newFormat = Column(String(128), nullable=False)
    oldFormat = Column(String(128))
    status    = Column(String(128), nullable=False, default='uploaded')
    timeStamp = Column(DateTime(), default=datetime.datetime.utcnow)
    
    user = Column(Integer, ForeignKey('users.id'))
    
    def __repr__(self):
        return f"{self.fileName} - {self.newFormat} - {self.timeStamp} - {self.status}"
    
class FileSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = File
        include_relationships = True
        load_instance = True

class create_all():
    engine = get_engine()
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)