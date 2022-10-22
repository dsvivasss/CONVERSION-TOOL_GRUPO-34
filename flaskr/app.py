import email
import imp
from flaskr import create_app
from .models import db, File, User
# from authorization.models import User
# from .models import AlbumSchema, CancionSchema, UsuarioSchema
from flask_restful import Api, Resource
# from .vistas import VistaCanciones, VistaCancion, VistaLogIn, VistaSignIn, VistaAlbum, VistaAlbumsUsuario, VistaCancionesAlbum
from .vistas import LoginView, SignUpView, TasksView
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
# api.add_resource(VistaCanciones, '/canciones/')
# api.add_resource(VistaCancion, '/cancion/<int:id_cancion>/')
# api.add_resource(VistaSignIn, '/signin/')
# api.add_resource(VistaLogIn, '/login/')
# api.add_resource(VistaAlbumsUsuario, '/usuario/<int:id_usuario>/albumes')
# api.add_resource(VistaAlbum, '/album/<int:id_album>/')
# api.add_resource(VistaCancionesAlbum, '/album/<int:id_album>/canciones/')

api.add_resource(LoginView, '/api/auth/login/')
api.add_resource(SignUpView, '/api/auth/signup/')
api.add_resource(TasksView, '/api/tasks/')
jwt = JWTManager(app)

#Prueba
with app.app_context():
    pass
    
    u = User(username='Juan', password='12345', email='juan@gmail.com')
    
    db.session.add(u)
    db.session.commit()
    
    file1 = File(fileName='file1', fileFormat='pdf', status='pending', path='C:/Users/Juan/Desktop/file1.pdf', user = u.id)
    file2 = File(fileName='file2', fileFormat='pdf', status='pending', path='C:/Users/Juan/Desktop/file2.pdf', user = u.id)
    
    db.session.add_all([file1, file2])
    db.session.commit()
    
class VistaPuntaje(Resource):

    def post(self):
        
        return {'puntaje': 5}
        
        # content = requests.get(f'http://127.0.0.1:5000/cancion/{id_cancion}')
        
        # if content.status_code == 404:
        #     return content.json(), 404
        # else:
        #     cancion = content.json()
        #     cancion['puntaje'] = request.json['puntaje']
        #     args = (cancion,)
        #     registrar_puntaje.apply_async(args=args)
        #     return json.dumps(cancion)
        
api.add_resource(VistaPuntaje, '/cancion/')