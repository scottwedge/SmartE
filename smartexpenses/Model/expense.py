from smartexpenses import db

class Expense(db.Model):
    __tablename__ = 'expenses'
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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


    def save_to_db(self):
        db.session.add(self)
        db.seesion.commit()

    @classmethod
    def find_by_title(cls,title):
        return cls.query.filter_by(title=title).all()
    
    @classmethod
    def return_all(cls):
        def to_json(x):
            return{
                'title':x.title,
                'private':x.private,
                'currency':x.currency,
                'value':x.value,
                'valueUSD':x.valueUSD,
                'lattitude':x.lattitude,
                'longitude':x.longitude,
                'address':x.address,
                'categoryID':x.categoryID,
                'date':x.date,
                'user_id':x.user_id

            }
        return {'expenses': list(map(lambda x: to_json(x), Expense.query.all()))}
