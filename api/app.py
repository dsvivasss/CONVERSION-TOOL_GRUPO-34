from . import create_app
from .models import db, File, User
# from authorization.models import User
# from .models import AlbumSchema, CancionSchema, UsuarioSchema
from flask_restful import Api, Resource
# from .vistas import VistaCanciones, VistaCancion, VistaLogIn, VistaSignIn, VistaAlbum, VistaAlbumsUsuario, VistaCancionesAlbum
from .vistas import LoginView, SignUpView, TasksView, UniqueTaskView, FilesView, ModifyFileView
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = create_app('default')

# Context is a dictionary that is used to store application-specific data.

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)

api.add_resource(LoginView, '/api/auth/login/')
api.add_resource(SignUpView, '/api/auth/signup/')
api.add_resource(TasksView, '/api/tasks/')
api.add_resource(UniqueTaskView, '/api/tasks/<int:id>/')
api.add_resource(FilesView, '/api/files/<string:filename>/')
api.add_resource(ModifyFileView, '/api/file/<string:id>/')
jwt = JWTManager(app)

#Prueba
with app.app_context():
    # consumer.run()
    pass

