from flask import Flask
from smartexpenses.routes import root
import os

DB_URI = os.environ.get('CLEARDB_DATABASE_URL')
print("HAHÓÓÓÓÓÓÓÓÓ")
print(DB_URI)

app = Flask(__name__)
app.register_blueprint(root)