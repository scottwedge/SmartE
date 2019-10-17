from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from smartexpenses.routes import root
import os

DB_URI = os.environ.get('CLEARDB_DATABASE_URL')

app = Flask(__name__)
app.register_blueprint(root)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI

db = SQLAlchemy(app)