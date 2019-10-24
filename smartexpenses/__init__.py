from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import os

ON_HEROKU = 'ON_HEROKU' in os.environ

if ON_HEROKU:
    DB_URL = os.environ.get('CLEARDB_DATABASE_URL')
    print('HELLOOO')
    print(DB_URL)
else:
    from dotenv import load_dotenv
    load_dotenv()
    DB_URL = os.getenv('MYSQL_URL')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

api = Api(app)

from smartexpenses.Controller.root import root
from smartexpenses.Controller.user_controller import user_routes
       
app.register_blueprint(root)      
api.add_resource(user_routes.UserRegistration,  '/registration')
api.add_resource(user_routes.UserLogin,         '/login')
api.add_resource(user_routes.UserLogoutAccess,  '/logout/access')
api.add_resource(user_routes.UserLogoutRefresh, '/logout/refresh')
api.add_resource(user_routes.TokenRefresh,      '/token/refresh')
api.add_resource(user_routes.AllUsers,          '/users')
api.add_resource(user_routes.SecretResource,    '/secret')

db.create_all()
