import datetime
import io
import json
import os
from datetime import datetime

import flask
import jwt
from flask import request, send_file
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource
from google.cloud import pubsub_v1, storage
from werkzeug.utils import secure_filename

from ..decorators import token_required
from ..models import File, FileSchema, User, UserSchema, session

project_id = os.environ['proyect-id']
topic_id = os.environ['topic-id']
upload_bucket_name= os.environ['upload-bucket-name']
download_bucket_name= os.environ['download-bucket-name']

# project_id = 'convertor-tool'
# topic_id = 'convert_song'
# upload_bucket_name= 'original-song'
# download_bucket_name= 'convert-song'

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)
storage_client = storage.Client()

upload_bucket = storage_client.bucket(upload_bucket_name)
download_bucket = storage_client.bucket(download_bucket_name)

file_schema = FileSchema()
user_schema = UserSchema()
valid_token_seconds = 3600

# Allowed audio formats
ALLOWED_EXTENSIONS = {'MP3', 'ACC', 'OGG', 'WAV', 'WMA', 'mp3', 'acc', 'ogg', 'wav', 'wma'}

def json_serializer(data):
    return json.dumps(data).encode("utf-8")

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

        blob = upload_bucket.blob(f.filename)
        blob.upload_from_file(f)
        
        user = session.query(User).filter_by(username=username).first()
        file = File(fileName=f.filename, newFormat=newFormat, oldFormat=oldFormat, user=user.id)
        session.add(file)
        session.commit()

        data = {'fileName': f.filename, 'newFormat': newFormat, 'oldFormat': oldFormat, 'username': username, 'id': file.id}
        future = publisher.publish(topic_path, json_serializer(data))
        print(future.result())
        
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

        if file.status == "uploaded":
            return {'message': 'File can not be deleted'}, 404

        if file is None:
            return {'message': 'File not found'}, 404
        
        session.delete(file)
        session.commit()
        
        return {}, 204
    
class ModifyFileView(Resource):
    
    def put(self, id):
        file = session.query(File).get(id)
        if file is None:
            return {'message': 'File not found'}, 404
        
        file.status = 'processed'
        
        session.commit()
        
        # SEND EMAIL TO USER
        
        return {'message': 'success'}, 200
        
class FilesViewUpload(Resource):
    
    @token_required
    def get(self, id):
        file = session.query(File).get(id)
        if file is None:
            return {'message': 'File not found'}, 404
        
        blob = upload_bucket.get_blob(file.fileName)
        bites = blob.download_as_string()
        test = io.BytesIO(bites)
        test.seek(0)
        return send_file(test, mimetype=f'audio/{file.oldFormat}', as_attachment=True, download_name=f'{file.fileName}')
class FilesViewConvert(Resource):
    
    @token_required
    def get(self, id):
        file = session.query(File).get(id)
        if file is None:
            return {'message': 'File not found'}, 404
        
        name = file.fileName.split('.')
        new_name= name[0] + '.'+ file.newFormat

        blob = download_bucket.get_blob(new_name)
        bites = blob.download_as_string()
        test = io.BytesIO(bites)
        test.seek(0)
        return send_file(test, mimetype=f'audio/{file.oldFormat}', as_attachment=True, download_name=f'{new_name}')

class LoginView(Resource):
    
    def post(self):
        username = request.json.get('username', None)
        
        # check if username exists in database
        user = session.query(User).filter_by(username=username).first()
        
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