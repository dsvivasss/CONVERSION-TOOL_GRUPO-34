import jwt
import datetime
from sql_api import crud
from flask import request
from flask_restful import Resource
from sql_api.database import SessionLocal


valid_token_seconds = 3600

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class LoginView(Resource):
    
    def post(self):
        db = next(get_db())
        username = request.json.get('username', None)
        
        # check if username exists in database
        user = crud.get_user_username(db, username)
        
        if user is None:
            return {'message': 'User not found'}, 401
        
        if user.password != request.json.get('password', None):
            return {'message': 'Invalid password'}, 401
        
        timestamp = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=valid_token_seconds)
        base_token = {
            'iat': timestamp,
            'exp': timestamp + datetime.timedelta(seconds=valid_token_seconds),
            'sub': username,
            'iss': 'www.test.com',
            # 'permissions': device_found['permissions']
        }
        encoded_jwt = jwt.encode(base_token, "secret", algorithm="HS256")
        response = {'token': encoded_jwt}
        return response, 200