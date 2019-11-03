from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os

ON_HEROKU = 'ON_HEROKU' in os.environ

if ON_HEROKU:
    DB_URL = os.environ.get('CLEARDB_DATABASE_URL')
else:
    from dotenv import load_dotenv
    load_dotenv()
    DB_URL = os.getenv('MYSQL_URL')

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
jwt = JWTManager(app)

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['refresh']
app.config['PROPAGATE_EXCEPTIONS'] = True

@app.before_first_request
def create_tables():
    db.create_all()

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return Model.RevokedTokenModel.is_jti_blacklisted(jti)

from smartexpenses.Controller.root import root
from smartexpenses.Controller import auth_controller
from smartexpenses.Controller import expenses_controller

app.register_blueprint(root)
api.add_resource(auth_controller.UserRegistration,  '/register')
api.add_resource(auth_controller.UserLogin,         '/login')
api.add_resource(auth_controller.UserLogoutRefresh, '/logout')
api.add_resource(auth_controller.AllUsers,          '/users')
api.add_resource(auth_controller.SecretResource,    '/secret')

api.add_resource(expenses_controller.AllExpenses,   '/expenses')
api.add_resource(expenses_controller.AddExpense,   '/addexpense')
api.add_resource(expenses_controller.GetExpenseById,   '/expenses/<id>')
