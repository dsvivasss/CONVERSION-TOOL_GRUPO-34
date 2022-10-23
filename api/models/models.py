from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(32))
    email = db.Column(db.String(256))

    def __repr__(self):
        return f"{self.username} - {self.email}"
    
class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True
    
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fileName = db.Column(db.String(128))
    newFormat = db.Column(db.String(128))
    # oldFormat = db.Column(db.String(128))
    timeStamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    status = db.Column(db.String(128), default='uploaded')
    
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f"{self.fileName} - {self.newFormat} - {self.timeStamp} - {self.status}"
    
class FileSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = File
        include_relationships = True
        load_instance = True