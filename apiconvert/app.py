from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from vistas.Login import LoginView
from vistas.SignUp import SignUpView
from vistas.Tasks import TasksView
from vistas.Task import TaskView
from vistas.FilesUpload import FilesUploadView
from vistas.FilesConvert import FilesConvertView
from vistas.ModifyFile import ModifyFileView

app = Flask(__name__)
app_context = app.app_context()
app_context.push()
cors = CORS(app)
jwt = JWTManager(app)
api = Api(app)
api.add_resource(LoginView, '/api/auth/login')
api.add_resource(SignUpView, '/api/auth/signup')
api.add_resource(TasksView, '/api/tasks')
api.add_resource(TaskView, '/api/tasks/<int:id>')
api.add_resource(FilesUploadView, '/api/files/<int:id>/original')
api.add_resource(FilesConvertView, '/api/files/<int:id>/convert')
api.add_resource(ModifyFileView, '/api/file/<string:id>')