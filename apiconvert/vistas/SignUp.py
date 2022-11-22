from flask import request
from sql_api import crud, models
from flask_restful import Resource
from sql_api.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class SignUpView(Resource):
    
    def post(self):
        db = next(get_db())
        username = request.json.get('username', None)
        password1 = request.json.get('password1', None)
        password2 = request.json.get('password2', None)
        email = request.json.get('email', None)
        
        # check if username exists in database       
        userByUsername = crud.get_user_username(db, username)
        userByEmail = crud.get_user_email(db, email)
        
        if userByUsername is not None:
            return {'message': 'Username already exists'}, 401
        
        if userByEmail is not None:
            return {'message': 'Email already exists'}, 401
        
        if password1 != password2:
            return {'message': 'Passwords do not match'}, 401
        
        user = models.User(username=username, password=password1, email=email)
        crud.create_user(db,user)
        
        return {'message': 'User created'}, 200