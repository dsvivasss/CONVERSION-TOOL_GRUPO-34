
from flask import request, send_file
from kafka import KafkaProducer, KafkaConsumer
import jwt
from ..models import File, FileSchema, User, UserSchema, session
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

# Allowed audio formats
ALLOWED_EXTENSIONS = {'MP3', 'ACC', 'OGG', 'WAV', 'WMA', 'mp3', 'acc', 'ogg', 'wav', 'wma', 'pdf'}

def json_serializer(data):
    return json.dumps(data).encode("utf-8")

# producer = KafkaProducer(
#     bootstrap_servers=['localhost:9092'],
#     value_serializer=json_serializer,
#     # partitioner=get_partition
#     )

class TasksView(Resource):
    
    @token_required
    def get(self):
        # get username from token
        token = request.headers.get('Authorization').split(' ')[1]
        decoded_token = jwt.decode(token, "secret", algorithms=["HS256"])
        username = decoded_token['sub']
        
        if username == 'conversion':
            files = session.query(File).all()
            return file_schema.dump(files, many=True)
        
        userId = session.query(User).filter_by(username=username).first().id
        files = session.query(File).filter_by(user=userId).all()
        
        return file_schema.dump(files, many=True), 200
    
    @token_required
    def post(self):
        f = request.files['fileName']
        newFormat = request.form['newFormat']
        
        oldFormat = f.filename.rsplit('.', 1)[1].lower()
        
        if oldFormat not in ALLOWED_EXTENSIONS:
            return {'message': 'File format not allowed, allowed formats: MP3, ACC, OGG, WAV, WMA'}, 400
        
        token = request.headers.get('Authorization').split(' ')[1]
        decoded_token = jwt.decode(token, "secret", algorithms=["HS256"])
        username = decoded_token['sub']
        
        UPLOAD_FOLDER = f'../uploads'
        
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        
        f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
        
        user = session.query(User).filter_by(username=username).first()
        file = File(fileName=f.filename, newFormat=newFormat, oldFormat=oldFormat, user=user.id)
        session.add(file)
        session.commit()
        
        # producer.send('conversion', value={'fileName': f.filename, 'newFormat': newFormat, 'oldFormat': oldFormat})
        
        return {'message': 'file uploaded successfully'}
    
class UniqueTaskView(Resource):
    
    @token_required
    def get(self, id):
        file = session.query(File).get(id)
        if file is None:
            return {'message': 'File not found'}, 404
        
        return file_schema.dump(file), 200
    
    @token_required
    def put(self, id):
        file = session.query(File).get(id)
        if file is None:
            return {'message': 'File not found'}, 404
        
        file.status = 'uploaded'
        file.newFormat = request.json.get('newFormat', None)
        
        session.commit()
        
        return file_schema.dump(file), 200
    
    @token_required
    def delete(self, id):
        file = session.query(File).get(id)
        if file is None:
            return {'message': 'File not found'}, 404
        
        session.delete(file)
        session.commit()
        
        return {}, 204
    
class ModifyFileView(Resource):
    @token_required
    def put(self, id):
        file = session.query(File).get(id)
        if file is None:
            return {'message': 'File not found'}, 404
        
        file.status = 'processed'
        
        session.commit()
        
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
        user = session.query(User).filter_by(username=username).first()
        
        if user is None:
            return {'message': 'User not found'}, 401
        
        if user.password != request.json.get('password', None):
            return {'message': 'Invalid password'}, 401
        
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
        userByUsername = session.query(User).filter_by(username=username).first()
        userByEmail = session.query(User).filter_by(email=email).first()
        
        if userByUsername is not None:
            return {'message': 'Username already exists'}, 401
        
        if userByEmail is not None:
            return {'message': 'Email already exists'}, 401
        
        if password1 != password2:
            return {'message': 'Passwords do not match'}, 401
        
        new_user = User(username=username, password=password1, email=email)
        session.add(new_user)
        session.commit()
        
        return {'message': 'User created'}, 200