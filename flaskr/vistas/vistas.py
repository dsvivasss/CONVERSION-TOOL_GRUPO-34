
from flask import request
import jwt
from ..models import db, File, FileSchema, User, UserSchema
from flask_restful import Resource
from flask_jwt_extended import jwt_required, create_access_token
import datetime
from ..decorators import token_required

file_schema = FileSchema()
user_schema = UserSchema()

class TasksView(Resource):
    
    @token_required
    def get(self):
        # get username from token
        token = request.headers.get('Authorization').split(' ')[1]
        decoded_token = jwt.decode(token, "secret", algorithms=["HS256"])
        username = decoded_token['sub']
        
        userId = User.query.filter_by(username=username).first().id
        files = File.query.filter_by(user=userId, status='processed').all()
        
        return file_schema.dump(files, many=True), 200

class LoginView(Resource):
    
    def post(self):
        username = request.json.get('username', None)
        
        # check if username exists in database
        user = User.query.filter_by(username=username).first()
        
        if user is None:
            return 'User not found', 401
        
        if user.password != request.json.get('password', None):
            return 'Invalid password', 401
        
        timestamp = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=30)
        base_token = {
            'iat': timestamp,
            'exp': timestamp + datetime.timedelta(seconds=30),
            'sub': username,
            'iss': 'www.test.com',
            # 'permissions': device_found['permissions']
        }
        encoded_jwt = jwt.encode(base_token, "secret", algorithm="HS256")
        response = {'token': encoded_jwt}
        return response, 200
    
class SignUpView(Resource):
    
    def post(self):
        username = request.json.get('username', None)
        password1 = request.json.get('password1', None)
        password2 = request.json.get('password2', None)
        email = request.json.get('email', None)
        
        # check if username exists in database
        userByUsername = User.query.filter_by(username=username).first()
        userByEmail = User.query.filter_by(email=email).first()
        
        if userByUsername is not None:
            return {'message': 'Username already exists'}, 401
        
        if userByEmail is not None:
            return {'message': 'Email already exists'}, 401
        
        if password1 != password2:
            return {'message': 'Passwords do not match'}, 401
        
        new_user = User(username=username, password=password1, email=email)
        db.session.add(new_user)
        db.session.commit()
        
        return {'message': 'User created'}, 200