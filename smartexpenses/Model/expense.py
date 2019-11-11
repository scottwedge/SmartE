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
    latitude = db.Column(db.Float, nullable=False)
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
        db.session.close()

    @classmethod
    def update_to_db(cls,newexpense):
        db.session.bulk_update_mappings(Expense, newexpense)
        db.session.commit()
        db.session.close()

    @classmethod
    def return_all(cls,current_id):
        def to_json(x):                 
            return {
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
        return {'expenses': list(map(lambda x: to_json(x), Expense.query.all()))}

    @classmethod
    def find_by_id(cls, id):
        expense = db.session.query(Expense).filter(Expense.id == id).first()
        return {
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

    @classmethod
    def recent_expense(cls, num, id):
        # currentId = db.session.query(User).filter(User.email == token_email).first().id
        expense = db.session.query(Expense).filter(Expense.user_id == id).limit(num)
        allImageUrl = [
            {
            "id":1,
            "url":"https://pic2.zhimg.com/v2-1fd63894af1d05828fc4cf987af517b1_1200x500.jpg"
            },
             {
            "id":2,
            "url":"https://www.obonparis.com/uploads/BORZE%20RESTAURANT/MIS03809.jpg"
            }, 
            {
            "id":3,
            "url":"http://www.xwlxw.com/uploads/allimg/150928/7-15092Q15159544.png"
            }, 
            {
            "id":4,
            "url":"https://www.obonparis.com/uploads/NEW%20YORK%20CAFE%20BUDAPEST/NEW%20YORK%20CAFE-0584.jpg"
            }, 
            {
            "id":5,
            "url":"hhttps://www.obonparis.com/uploads/NEW%20YORK%20CAFE%20BUDAPEST/NEW%20YORK%20CAFE-0555.jpg"
            },
             {
            "id":6,
            "url":"https://www.obonparis.com/uploads/BUDAPEST%20BEST%20THINGS/BAC02566.jpg"
            }, 
            {
            "id":7,
            "url":"https://www.obonparis.com/uploads/BUDAPEST%20BEST%20THINGS/BAC02270.jpg"
            } ]
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
                'date':x.date.strftime('%Y-%m-%d %H:%M:%S'),
                'user_id':x.user_id

            }
        return {
            'expenses': list(map(lambda x: to_json(x), expense)),
            'images' :  allImageUrl
        }

    @classmethod
    def find_id_by_email(cls,email):    
        current_user = db.session.query(User).filter(User.email == email).first()
        current_id = current_user.id
        return current_id

    @classmethod
    def delete_by_id(cls,id):
        delete_expense = db.session.query(Expense).filter(Expense.id == id).first() 
        db.session.delete(delete_expense)
        db.session.commit()