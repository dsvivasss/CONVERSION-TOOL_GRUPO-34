from sql_api import crud
from flask_restful import Resource
from sql_api.database import SessionLocal

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
        
        file = crud.update_file_status(db, 'processed', file.id)
        
        return {'message': 'success'}, 200
 