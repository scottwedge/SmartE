from flask_restful import Resource, reqparse
from binascii import hexlify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt
from smartexpenses.Model.expense import Expense

class AllExpenses(Resource):
    def get(self):
        return {'message': 'List of expenses'}

    def delete(self):
        return {'message': 'Delete all expenses'}