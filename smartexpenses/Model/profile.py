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
    profile_image =         db.Column(db.Text, nullable=False)
    user_id =               db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, index=True, nullable=False)
    user =                  db.relationship('User', backref='profiles', lazy=True)
   
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def update_profile_by_user_id(cls, user_id, data):
        profile = cls.query.filter_by(user_id = user_id).first()
        profile.color = data["color"]
        profile.notifications = bool(data["notifications"])
        profile.profile_image = bytes(data["profile_image"], encoding='utf8') 
        profile.num_latest_spendings = data["num_latest_spendings"]
        db.session.commit()
        db.session.close()

    @classmethod
    def update_total_spendings(cls, user_id):
        total_spendings = Profile.get_total_spendings(user_id)  
        profile = cls.query.filter_by(user_id=user_id).scalar()
        profile.total_spendings = total_spendings
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
        profile = cls.query.filter_by(user_id = user_id).first()
        if profile:
            return {
                'user_id' : profile.user_id,
                'total_spendings' : Profile.call_total_spendings(user_id),
                'color' : profile.color,
                'notifications' : profile.notifications,
                'num_latest_spendings' : profile.num_latest_spendings,
                'profile_image' : json.dumps((profile.profile_image).decode("utf-8")),
                'privacy_url' : 'https://www.opentracker.net/article/how-write-website-privacy-policy ',
                'terms_and_conditions_url' : 'https://help.opentracker.net/collection/11-help ' 
            }
