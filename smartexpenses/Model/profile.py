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
    profile_image =         db.Column(db.String(200), nullable=False)
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
    def update_total_spendings(cls, user_id, value):
        profile = cls.query.filter_by(user_id=user_id).scalar()
        profile.total_spendings += value
        profile.update_to_db()
       
    @classmethod
    def get_total_spendings(cls,user_id):
        total_spendings = 0
        expenses = db.session.query(Expense).filter(Expense.user_id==user_id).all()
        for expense in expenses:
            total_spendings += expense.value
        return total_spendings
      
    @classmethod
    def return_profile_by_user_id(cls, user_id):
        profile = cls.query.filter_by(user_id=user_id).all()
        if profile:
            def to_json(x):
                return{
                    'user_id':x.user_id,
                    'total_spendings': x.total_spendings,
                    'color':x.color,
                    'notifications':x.notifications,
                    'num_latest_spendings':x.num_latest_spendings,
                    'profile_image':x.profile_image,
                    'privacy_url ':'privacy_url ',
                    'terms_and_conditions_url ': 'terms_and_conditions_url '
                }          
            return list(map(lambda x: to_json(x), profile))
        else:
            return 'no such this user profile'
