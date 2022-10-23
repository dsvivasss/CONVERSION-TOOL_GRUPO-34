
from flask import request, send_file
from kafka import KafkaProducer, KafkaConsumer
import jwt
from ..models import db, File, FileSchema, User, UserSchema
from flask_restful import Resource
from flask_jwt_extended import jwt_required, create_access_token
from werkzeug.utils import secure_filename
import datetime
from ..decorators import token_required
import os
import urllib.parse
import json

file_schema = FileSchema()
user_schema = UserSchema()
valid_token_seconds = 3600

def json_serializer(data):
    return json.dumps(data).encode("utf-8")

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=json_serializer)

class TasksView(Resource):
    
    @token_required
    def get(self):
        # get username from token
        token = request.headers.get('Authorization').split(' ')[1]
        decoded_token = jwt.decode(token, "secret", algorithms=["HS256"])
        username = decoded_token['sub']
        
        if username == 'conversion':
            files = File.query.all()
            return file_schema.dump(files, many=True)
        
        userId = User.query.filter_by(username=username).first().id
        files = File.query.filter_by(user=userId).all()
        
        return file_schema.dump(files, many=True), 200
    
    @token_required
    def post(self):
        f = request.files['fileName']
        newFormat = request.form['newFormat']
        
        token = request.headers.get('Authorization').split(' ')[1]
        decoded_token = jwt.decode(token, "secret", algorithms=["HS256"])
        username = decoded_token['sub']
        
        UPLOAD_FOLDER = f'../uploads'
        
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        
        f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
        
        user = User.query.filter_by(username=username).first()
        file = File(fileName=f.filename, newFormat=newFormat, user=user.id)
        db.session.add(file)
        db.session.commit()
        
        producer.send('convert_song', value={'fileName': f.filename, 'newFormat': newFormat, 'username': username, 'id': file.id})
        
        return {'message': 'file uploaded successfully'}
    
class UniqueTaskView(Resource):
    
    @token_required
    def get(self, id):
        file = File.query.get(id)
        if file is None:
            return {'message': 'File not found'}, 404
        
        return file_schema.dump(file), 200
    
    @token_required
    def put(self, id):
        file = File.query.get(id)
        if file is None:
            return {'message': 'File not found'}, 404
        
        file.status = 'uploaded'
        file.newFormat = request.json.get('newFormat', None)
        
        db.session.commit()
        
        return file_schema.dump(file), 200
    
    @token_required
    def delete(self, id):
        file = File.query.get(id)
        if file is None:
            return {'message': 'File not found'}, 404
        
        db.session.delete(file)
        db.session.commit()
        
        return {}, 204
    
class ModifyFileView(Resource):
    
    def put(self, id):
        file = File.query.get(id)
        if file is None:
            return {'message': 'File not found'}, 404
        
        file.status = 'processed'
        
        db.session.commit()
        
        # SEND EMAIL TO USER
        
        return {'message': 'success'}, 200
        
class FilesView(Resource):
    
    @token_required
    def get(self, filename):
        
        UPLOAD_FOLDER = f'../uploads'
        
        filenameEncoded = urllib.parse.quote(filename.encode('utf8'))
        
        return send_file(os.path.join(UPLOAD_FOLDER, filenameEncoded)) #, as_attachment=True

class LoginView(Resource):
    
    def post(self):
        username = request.json.get('username', None)
        
        # check if username exists in database
        user = User.query.filter_by(username=username).first()
        
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