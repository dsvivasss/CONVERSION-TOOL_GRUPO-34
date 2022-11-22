import json

from sql_api import crud
from flask_restful import Resource
from google.cloud import pubsub_v1
from sql_api.database import SessionLocal
from environments import project_id, email_topic_name

publisher = pubsub_v1.PublisherClient()
email_topic = publisher.topic_path(project_id, email_topic_name)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ModifyFileView(Resource):
    
    def put(self, id):
        db = next(get_db())
        file = crud.get_file_id(db, id)
        if file is None:
            return {'message': 'File not found'}, 404

        user = crud.get_user_id(db, file.user)
        
        file = crud.update_file_status(db, 'processed', file.id)
        print(file)
        data = {'fileName': file.fileName, 'status': 'processed', 'email': user.email}
        publisher.publish(email_topic, json.dumps(data).encode("utf-8"))
        
        return {'message': 'success'}, 200
 