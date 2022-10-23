<<<<<<< HEAD
from mimetypes import init
from api import create_app
<<<<<<< HEAD
<<<<<<< HEAD
from .models import create_all
=======
=======
from . import create_app
>>>>>>> origin/TasksMateo
from .models import db, File, User
>>>>>>> origin/convert_setup
=======
from .models import create_all
>>>>>>> origin/develop
from flask_restful import Api, Resource
from .vistas import LoginView, SignUpView, TasksView, UniqueTaskView, ModifyFileView, FilesViewUpload, FilesViewConvert
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = create_app('default')

# Context is a dictionary that is used to store application-specific data.
app_context = app.app_context()
app_context.push()

create_all()
cors = CORS(app)
api = Api(app)

api.add_resource(LoginView, '/api/auth/login')
api.add_resource(SignUpView, '/api/auth/signup')
api.add_resource(TasksView, '/api/tasks')
api.add_resource(UniqueTaskView, '/api/tasks/<int:id>')
api.add_resource(FilesViewUpload, '/api/files/<int:id>/original')
api.add_resource(FilesViewConvert, '/api/files/<int:id>/convert')
api.add_resource(ModifyFileView, '/api/file/<string:id>')
jwt = JWTManager(app)

#Prueba
with app.app_context():
    # consumer.run()
    pass
