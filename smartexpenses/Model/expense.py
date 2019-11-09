from smartexpenses import db
from smartexpenses.Model.user import User
import datetime
import json

class Expense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    private = db.Column(db.Boolean, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    value = db.Column(db.Float, nullable=False)
    valueUSD = db.Column(db.Float, nullable=False)
    lattitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    categoryID = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False,)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __iter__(self):
        return self

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    
    @classmethod
    def return_all(cls):
        def to_json(x):                 
            try:
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
                    'date':x.date.strftime('%Y-%m-%d %H:%M:%S'),
                    'user_id':x.user_id

                }
            except:
                return{'message':'I cannot get this message'}
        return {'expenses': list(map(lambda x: to_json(x), Expense.query.all()))}


    @classmethod
    def find_by_id(cls,id):
        expense = db.session.query(Expense).filter(Expense.id == id).first()
        try:
            return{
                'title':expense.title,
                'private':expense.private,
                'currency':expense.currency,
                'value':expense.value,
                'valueUSD':expense.valueUSD,
                'lattitude':expense.lattitude,
                'longitude':expense.longitude,
                'address':expense.address,
                'categoryID':expense.categoryID,
                'date':expense.date.strftime('%Y-%m-%d %H:%M:%S'),
                'user_id':expense.user_id
            }
        except:
            return{'message':'I cannot get this message'}

    @classmethod
    def find_id_by_email(cls,email):    
        current_user = db.session.query(User).filter(User.email == email).first()
        current_id = current_user.id
        print(current_id)
        return current_id

        


