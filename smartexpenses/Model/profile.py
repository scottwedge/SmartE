from smartexpenses import db
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from smartexpenses.Model.user import User
from smartexpenses.Model.expense import Expense
import json

class Profile(db.Model):
    __tablename__ = 'profiles'
    id =                    db.Column(db.Integer, primary_key=True)
    total_spendings =       db.Column(db.Float, nullable=False)
    color =                 db.Column(db.String(100),nullable=False)
    notifications =         db.Column(db.Boolean, nullable=False)
    num_latest_spendings =  db.Column(db.Integer, nullable=False)
    profile_image =         db.Column(db.LargeBinary(16777216), nullable=False)
    user_id =               db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, index=True, nullable=False)
    user =                  db.relationship('User', backref='profiles', lazy=True)
   
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def update_to_db(self):
        db.session.commit()
        db.session.close()
        
    @classmethod
    def str_to_bool(cls,str):
        return True if str.lower() == 'true' else False

    @classmethod
    def update_profile_by_user_id(cls,user_id,data):
        cur_profile = cls.query.filter_by(user_id=user_id).first()
        cur_profile.color= data["color"]
        cur_profile.notifications = cls.str_to_bool(data["notifications"])
        cur_profile.profile_image =     bytes(data["profile_image"], encoding='utf8') 
        cur_profile.num_latest_spendings = data["num_latest_spendings"]
        db.session.commit()
        db.session.close()


    @classmethod
    def update_total_spendings(cls, user_id):

        total_spendings = Profile.call_total_spendings(user_id)  
        prof = cls.query.filter_by(user_id=user_id).scalar()
        prof.total_spendings = total_spendings
        prof.update_to_db()
       
    @classmethod
    def call_total_spendings(cls,user_id):
        values = 0
        al_expense = db.session.query(Expense).filter(Expense.user_id==user_id).all()
        for a in al_expense:
            values += a.value
        print(values)
        return values
      
    @classmethod
    def return_profile_by_user_id(cls, user_id):
        profile = cls.query.filter_by(user_id=user_id).all()
        if profile:
            return{
               'user_id':profile[0].user_id,
                'total_spendings': Profile.call_total_spendings(user_id),
                'color':profile[0].color,
                'notifications':profile[0].notifications,
                'num_latest_spendings':profile[0].num_latest_spendings,
                'profile_image':json.dumps((profile[0].profile_image).decode("utf-8")),
                'privacy_url ':'https://www.opentracker.net/article/how-write-website-privacy-policy ',
                'terms_and_conditions_url ': 'https://help.opentracker.net/collection/11-help ' 
            }
        else:
            return 'Such profile does not exist'
