from flask_restful import Resource, reqparse, inputs
from binascii import hexlify
from flask_jwt_extended import jwt_refresh_token_required,get_jwt_identity
from smartexpenses.Model.expense import Expense
from smartexpenses.Model.user import User
from smartexpenses.Model.profile import Profile

parser = reqparse.RequestParser()
parser.add_argument('total_spendings', help = 'This field cannot be blank', required = True)
parser.add_argument('color',help='This field cannot be blank',required= True)
parser.add_argument('notifications',help='This field cannot be blank',required= True)


class GetProfile(Resource):
    @jwt_refresh_token_required
    def get(self):
        token_email = get_jwt_identity()
        user_id = User.find_by_email(token_email).id
        try:
            return {
                'messages' : Profile.return_profile_by_user_id(user_id),
                'status' : 0
            }
        except Exception as error:
            return { 
                'message': repr(error),
                'status' : 1
            }, 500

class UpdateProfile(Resource):
    @jwt_refresh_token_required
    def put(self,id):
        token_email = get_jwt_identity()
        user_id = User.find_by_email(token_email).id
