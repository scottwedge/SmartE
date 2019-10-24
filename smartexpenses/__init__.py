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
from smartexpenses.Controller import auth_controller

app.register_blueprint(root)      
api.add_resource(auth_controller.UserRegistration,  '/registration')
api.add_resource(auth_controller.UserLogin,         '/login')
api.add_resource(auth_controller.UserLogoutAccess,  '/logout/access')
api.add_resource(auth_controller.UserLogoutRefresh, '/logout/refresh')
api.add_resource(auth_controller.TokenRefresh,      '/token/refresh')
api.add_resource(auth_controller.AllUsers,          '/users')
api.add_resource(auth_controller.SecretResource,    '/secret')

db.create_all()
