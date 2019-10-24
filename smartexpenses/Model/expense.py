from smartexpenses import db

class Expense(db.Model):
    __tablename__ = 'expense'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(32), nullable=False)
    private = db.Column(db.Boolean, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    value = db.Column(db.Float, nullable=False)
    valueUSD = db.Column(db.Float, nullable=False)
    lattitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    categoryID = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)