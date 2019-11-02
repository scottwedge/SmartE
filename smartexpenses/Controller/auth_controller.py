from flask_restful import Resource, reqparse
from binascii import hexlify
from flask_jwt_extended import (create_refresh_token, jwt_required, jwt_refresh_token_required, 
                                get_jwt_identity, get_raw_jwt)
from smartexpenses.Model.user import User
from smartexpenses.Model import RevokedTokenModel

parser = reqparse.RequestParser()
parser.add_argument('email', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()

        if User.find_by_email(data['email']):
            return {
                'message': 'User {} already exists'.format(data['email']),
                'status' : 1
            }
        
        new_user = User(
            email = data['email'],
            password = User.generate_hash(data['password']),
            admin = 0
        )

        try:
            new_user.save_to_db()
            refresh_token = create_refresh_token(identity = data['email'])
            return {
                'message': 'User {} was created'.format(data['email']),
                'refresh_token': refresh_token,
                'status' : 0
                }
        except Exception as error:
            return {
                'message': repr(error),
                'status' : 1
            }, 500

class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = User.find_by_email(data['email'])

        if not current_user:
            return {
                'message': 'User {} doesn\'t exist'.format(data['email']),
                'status' : 1    
            }
        
        if User.verify_hash(data['password'], current_user.password):
            refresh_token = create_refresh_token(identity = data['email'])
            return {
                'message': 'Logged in as {}'.format(current_user.email),
                'refresh_token': refresh_token,
                'status' : 0
            }
        else:
            return {
                'message': 'Wrong credentials',
                'status' : 1
            }
      
class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {
                'message': 'Successful logout.',
                'status' : 0
            }
        except Exception as error:
            return {
                'message': repr(error),
                'status' : 1
            }, 500
         
class AllUsers(Resource):
    def get(self):
        return User.return_all()

    def delete(self):
        return User.delete_all()
      
class SecretResource(Resource):
    @jwt_refresh_token_required
    def get(self):
        return { 
            'message': 42,
            'status' : 0
        }, 200