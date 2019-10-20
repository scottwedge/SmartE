from smartexpenses import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True, unique=True, nullable=False)
    email = db.Column(db.String(100), index = True, unique=True, nullable=False)
    password= db.Column(db.String(128), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
    expenses = db.relationship('Expense', backref='user', lazy=True)

    def __init__(self, username, email, password, admin):
        self.username = username
        self.email = email
        self.password = password
        self.admin = admin

    def __rep__(self):
        return "User('{self.username}', '{self.email}')"