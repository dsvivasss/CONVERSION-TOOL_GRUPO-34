import io
import json
from flask import request
from flask_restful import Resource
from decorators import token_required
from sql_api import crud, schemas
from google.cloud import pubsub_v1, storage
from sql_api.database import SessionLocal
from environments import project_id, file_topic_name

publisher = pubsub_v1.PublisherClient()
file_topic = publisher.topic_path(project_id, file_topic_name)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TaskView(Resource):
    
    @token_required
    def get(self, id):
        db = next(get_db())
        file = crud.get_file_id(db, id)
        if file is None:
            return {'message': 'File not found'}, 404
        
        return file, 200
        #return file_schema.dump(file), 200
    
    @token_required
    def put(self, id):
        db = get_db()
        file = crud.get_file_id(db, id)
        if file is None:
            return {'messafile_topic_name not found'}, 404

        newFormat = request.json.get('newFormat', None)
        file = crud.update_file_status(db, 'uploaded', newFormat, file.id)
        
        data = {'fileName': file.filename, 'email': file.user.email}
        publisher.publish(file_topic, json.dumps(data).encode("utf-8"))
        return file, 200
        #return file_schema.dump(file), 200
    
    @token_required
    def delete(self, id):
        db = get_db()
        file = crud.get_file_id(db, id)

        if file.status == "uploaded":
            return {'message': 'File can not be deleted'}, 404

        if file is None:
            return {'message': 'File not found'}, 404

        crud.delete_file_id(file.id)
        return {}, 204
  