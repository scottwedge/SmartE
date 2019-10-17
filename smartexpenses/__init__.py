from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from smartexpenses.Controller.routes import root
import os

DB_URI = os.environ.get('CLEARDB_DATABASE_URL')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SECRET KEY'] = ''

app.register_blueprint(root)
db = SQLAlchemy(app)