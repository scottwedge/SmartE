from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

DB_URI = os.environ.get('CLEARDB_DATABASE_URL')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SECRET KEY'] = ''

db = SQLAlchemy(app)

from smartexpenses.Controller.root import root
from smartexpenses.Controller.user_controller import user_controller
app.register_blueprint(root)
app.register_blueprint(user_controller)

