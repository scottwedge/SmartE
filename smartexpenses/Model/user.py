from smartexpenses import db
from passlib.hash import pbkdf2_sha256 as sha256

class User(db.Model):
    __tablename__ = 'users'
    id =        db.Column(db.Integer, primary_key=True)
    email =     db.Column(db.String(100), index=True, unique=True, nullable=False)
    password =  db.Column(db.String(128), nullable=False)
    admin =     db.Column(db.Boolean, nullable=False)
    expenses =  db.relationship('Expense', backref='user', lazy=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'email': x.email,
                'password': x.password,
                'admin' : bool(x.admin)
            }
        try:
            return {
            'users': list(map(lambda x: to_json(x), User.query.all())),
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
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {
                'message' : '{} row(s) deleted'.format(num_rows_deleted),
                'status' : 0
            }
        except Exception as error:
            return {
                'message': repr(error),
                'status' : 1
            }

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)
