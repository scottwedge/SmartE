from flask import Flask
from smartexpenses.routes import root

app = Flask(__name__)
app.register_blueprint(root)