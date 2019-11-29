from smartexpenses import db
from smartexpenses.Model.user import User
import json

class Expense(db.Model):
    __tablename__ = 'expenses'
    id =            db.Column(db.Integer,     primary_key = True)
    title =         db.Column(db.String(100), nullable=False)
    private =       db.Column(db.Boolean,     nullable=False)
    currency =      db.Column(db.String(3),   nullable=False)
    value =         db.Column(db.Float,       nullable=False)
    valueUSD =      db.Column(db.Float,       nullable=False)
    latitude =      db.Column(db.Float,       nullable=False)
    longitude =     db.Column(db.Float,       nullable=False)
    address =       db.Column(db.String(100), nullable=False)
    categoryID =    db.Column(db.Integer,     nullable=False)
    date =          db.Column(db.Integer,     nullable=False)
    user_id =       db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  
    def save_to_db(self):
        db.session.add(self)    
        db.session.commit()
        db.session.close()

    def refresh_record_in_db(self):
        db.session.add(self)
        db.session.commit()
        db.session.flush()
        db.session.refresh(self)
        db.session.close()
        
    @classmethod
    def update_to_db(self):
        db.session.commit()
        db.session.close()

    @classmethod
    def return_all_by_user_id(cls, user_id):
        def to_json(x):                 
            return {
                'id' : x.id,
                'title' : x.title,
                'private' : x.private,
                'currency' : x.currency,
                'value' : x.value,
                'valueUSD' : x.valueUSD,
                'latitude' : x.latitude,
                'longitude' : x.longitude,
                'address' : x.address,
                'categoryID' : x.categoryID,
                'date' : x.date
            }
        # return list(map(lambda x: to_json(x), cls.query.filter_by(user_id=user_id).all()))
        return list(map(lambda x: to_json(x), cls.query.filter_by(user_id=user_id).order_by(Expense.date.desc()).all()))


    @classmethod
    def get_expense_location(cls,user_id):
        def to_json(x):
            return {
            'id' : x.id,
            'title' : x.title,  
            'latitude' : x.latitude,
            'longitude' : x.longitude,
            'categoryID' : x.categoryID
            }
        return list(map(lambda x: to_json(x), cls.query.filter_by(user_id=user_id).all()))


    @classmethod
    def return_all(cls):
        def to_json(x):                 
            return {
                'id' : x.id,
                'title' : x.title,
                'private' : x.private,
                'currency' : x.currency,
                'value' : x.value,
                'valueUSD' : x.valueUSD,
                'latitude' : x.latitude,
                'longitude' : x.longitude,
                'address' : x.address,
                'categoryID' : x.categoryID,
                'date' : x.date
            }
        return list(map(lambda x: to_json(x), cls.query.order_by(Expense.date.desc()).all()))

    @classmethod
    def find_by_userid_and_expenseid(cls, user_id, expense_id):
        pass
        expense = cls.query.filter_by(user_id = user_id, id=expense_id).first()
        if expense:
            return {
                'id' : expense.id,
                'title' : expense.title,
                'private' : expense.private,
                'currency' : expense.currency,
                'value' : expense.value,
                'valueUSD' : expense.valueUSD,
                'latitude' : expense.latitude,
                'longitude' : expense.longitude,
                'address' : expense.address,
                'categoryID' : expense.categoryID,
                'date' : expense.date
            }
        else:
            return 'No expense with id: {}'.format(expense_id)

    
    @classmethod
    def update_by_userid_and_expenseid(cls, user_id, expense_id, data):
        expense = cls.query.filter_by(user_id = user_id, id = expense_id).first()
        expense.title =      data['title']
        expense.private =    data['private']
        expense.currency =   data['currency']
        expense.value =      data['value']
        expense.valueUSD =   '%.2f'%(int(data['value'])/300)
        expense.latitude =   data['latitude']
        expense.longitude =  data['longitude']
        expense.address =    data['address']
        expense.categoryID = data['categoryID']
        expense.date =       data['date']
        db.session.commit()


    @classmethod
    def find_recents_by_user_id(cls, num, user_id):
        expenses = cls.query.filter_by(user_id = user_id).order_by(cls.date.desc()).limit(num).all() 
        # print(expenses)
        allImageUrl = [
            {
                "id" : 1,
                "imageUrl" : "https://pic2.zhimg.com/v2-1fd63894af1d05828fc4cf987af517b1_1200x500.jpg",
                "websiteUrl":"https://www.duol.hu/kultura/helyi-kultura/unnep-jozsef-nador-helyezte-el-a-pest-budai-lanchid-alapkovet-2987674/"
            },
            {
                "id" : 2,
                "imageUrl":"https://www.obonparis.com/uploads/BORZE%20RESTAURANT/MIS03809.jpg",
                "websiteUrl":"https://fuszereslelek.nlcafe.hu/2008/04/30/gulyas_6/"
            }, 
            {
                "id" : 3,
                "imageUrl" : "https://www.nationalgeographic.com/content/dam/travel/Guide-Pages/europe/budapest-travel.adapt.1900.1.jpg",
                "websiteUrl":"https://24.hu/fn/gazdasag/2016/02/05/igy-epult-fel-a-magyar-parlament-epulete-video/"
            }, 
            {
                "id" : 4,
                "imageUrl" : "https://www.obonparis.com/uploads/NEW%20YORK%20CAFE%20BUDAPEST/NEW%20YORK%20CAFE-0584.jpg",
                "websiteUrl":"https://www.newyorkcafe.hu/"

            }, 
            {
                "id" : 5,
                "imageUrl" : "https://www.obonparis.com/uploads/NEW%20YORK%20CAFE%20BUDAPEST/NEW%20YORK%20CAFE-0555.jpg",
                "websiteUrl":"https://www.newyorkcafe.hu/"
            },
             {
                "id" : 6,
                "imageUrl" : "https://www.obonparis.com/uploads/BUDAPEST%20BEST%20THINGS/BAC02566.jpg",
                "websiteUrl":"https://hungarytoday.hu/pedestrians-to-take-over-budapests-liberty-bridge-on-weekends-once-again/"
            }, 
            {
                "id" : 7,
                "imageUrl" : "https://static.femina.hu/husvet/kurtoskalacs_hazilag/kalacs_nagy.jpg",
                "websiteUrl":"https://femina.hu/husvet/kurtoskalacs_hazilag/"
            } 
        ]

        def to_json(x):                 
            return{
                'id' : x.id,
                'title' : x.title,
                'private' : x.private,
                'currency' : x.currency,
                'value' : x.value,
                'valueUSD' : x.valueUSD,
                'latitude' : x.latitude,
                'longitude' : x.longitude,
                'address' : x.address,
                'categoryID' : x.categoryID,
                'date' : x.date
            }
        # please clearful the place of return, do not change return 
        return {
            'expenses': list(map(lambda x: to_json(x), expenses)),
            'images':allImageUrl
        }

    @classmethod
    def delete_by_user_id(cls, user_id, expense_id):
        try:
            cls.query.filter_by(user_id = user_id, id = expense_id).delete()
            return {
                'message' : 'Expense {} was deleted'.format(expense_id),
                'status' : 0
            }
        except Exception as error:
            return {
                'message': repr(error),
                'status' : 1
            }
            
        
    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = cls.query().delete()
            db.session.commit()
            return {
                'message': '{} row(s) deleted'.format(num_rows_deleted),
                'status' : 0
            }
        except Exception as error:
            return {
                'message': repr(error),
                'status' : 1
            }
            
