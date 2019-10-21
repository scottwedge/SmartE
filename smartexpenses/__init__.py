from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

ON_HEROKU = 'ON_HEROKU' in os.environ

if ON_HEROKU:
    DB_URL = os.environ.get('CLEARDB_DATABASE_URL')
else:
    from dotenv import load_dotenv
    load_dotenv()
    DB_URL = os.getenv('MYSQL_URL')
    print(DB_URL)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from smartexpenses.Controller.root import root
from smartexpenses.Controller.user_controller import user_routes
       
app.register_blueprint(root)
app.register_blueprint(user_routes)

db.create_all()

