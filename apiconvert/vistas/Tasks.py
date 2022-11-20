import io
import jwt
import json
import datetime
from flask import request
from flask_restful import Resource
from decorators import token_required
from sql_api import crud, models
from google.cloud import pubsub_v1, storage
from sql_api.database import SessionLocal
from environments import project_id, file_topic_name, upload_bucket_name

storage_client = storage.Client()
publisher = pubsub_v1.PublisherClient()
file_topic_name = publisher.topic_path(project_id, file_topic_name)
upload_bucket = storage_client.bucket(upload_bucket_name)
ALLOWED_EXTENSIONS = {'MP3', 'ACC', 'OGG', 'WAV', 'WMA', 'mp3', 'acc', 'ogg', 'wav', 'wma'}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TasksView(Resource):
        
    @token_required
    def get(self):
        db = next(get_db())
        token = request.headers.get('Authorization').split(' ')[1]
        decoded_token = jwt.decode(token, "secret", algorithms=["HS256"])
        username = decoded_token['sub']
        
        if username == 'conversion':
            files = crud.get_files(db)
            return files, 200
            #return file_schema.dump(files, many=True)
        
        user_id = crud.get_user_username(db, username).id
        files = crud.get_file_user_id(db, user_id)
        
        return files, 200
        #return file_schema.dump(files, many=True), 200
    
    def post(self):
        db = next(get_db())
        f = request.files['fileName']
        newFormat = request.form['newFormat']
        
        oldFormat = f.filename.rsplit('.', 1)[1].lower()
        
        if oldFormat not in ALLOWED_EXTENSIONS:
            return {'message': 'File format not allowed, allowed formats: MP3, ACC, OGG, WAV, WMA'}, 400
        
        token = request.headers.get('Authorization').split(' ')[1]
        decoded_token = jwt.decode(token, options={'verify_signature': False, 'verify_aud': False, 'verify_nbf': False}, algorithms=["HS256"])
        username = decoded_token['sub']

        now = datetime.datetime.now()
        timestamp = datetime.datetime.timestamp(now)
        path_name = f'{timestamp}_{f.filename}'
        blob = upload_bucket.blob(path_name)
        blob.upload_from_file(f)
        
        user = crud.get_user_username(db, username)
        file = models.File(fileName=f.filename, newFormat=newFormat, oldFormat=oldFormat, user=user.id, pathName= path_name)
        file = crud.create_file(db,file)

        data = {'fileName': f.filename, 'newFormat': newFormat, 'oldFormat': oldFormat, 'username': username, 'id': file.id, 'pathName': path_name}
        publisher.publish(file_topic_name, json.dumps(data).encode("utf-8"))

        return {'message': 'file uploaded successfully'}
