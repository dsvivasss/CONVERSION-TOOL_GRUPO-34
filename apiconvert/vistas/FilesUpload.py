import io
from sql_api import crud
from flask import send_file
from flask_restful import Resource
from decorators import token_required
from sql_api.database import SessionLocal
from google.cloud import storage
from environments import upload_bucket_name

storage_client = storage.Client()
upload_bucket = storage_client.bucket(upload_bucket_name)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class FilesUploadView(Resource):
    
    @token_required
    def get(self, id):
        db = next(get_db())
        file = crud.get_file_id(db, id)
        if file is None:
            return {'message': 'File not found'}, 404
        
        blob = upload_bucket.get_blob(file.fileName)
        bites = blob.download_as_string()
        test = io.BytesIO(bites)
        test.seek(0)
        return send_file(test, mimetype=f'audio/{file.oldFormat}', as_attachment=True, download_name=f'{file.fileName}')