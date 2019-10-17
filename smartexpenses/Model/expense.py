
class Expense(db.Model):
    __tablename__ = 'expense'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(32))
    private = db.Column(db.Boolean)
    currency = db.Column(db.String(3))
    value = db.Column(db.Float)
    valueUSD = db.Column(db.Float)
    lattitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    address = db.Column(db.String(100))
    categoryID = db.Column(db.Integer)
    date = db.Column(db.DateTime)