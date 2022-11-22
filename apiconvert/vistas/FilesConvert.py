import io
from sql_api import crud
from google.cloud import storage
from flask_restful import Resource
from flask import send_file
from decorators import token_required
from sql_api.database import SessionLocal
from environments import download_bucket_name

storage_client = storage.Client()
download_bucket = storage_client.bucket(download_bucket_name)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class FilesConvertView(Resource):
    
    @token_required
    def get(self, id):
        db = next(get_db())
        file = crud.get_file_id(db, id)
        if file is None:
            return {'message': 'File not found'}, 404
        
        name = file.fileName.split('.')
        new_name= name[0] + '.'+ file.newFormat

        timestamp = file.pathName.split('_')[0]
        new_name= name[0] + '.'+ file.newFormat
        new_path = f'{timestamp}_{new_name}'

        blob = download_bucket.get_blob(new_path)
        bites = blob.download_as_string()
        test = io.BytesIO(bites)
        test.seek(0)
        return send_file(test, mimetype=f'audio/{file.newFormat}', as_attachment=True, download_name=f'{new_name}')
