from flask_restful import Resource, reqparse, inputs
from binascii import hexlify
from flask_jwt_extended import jwt_refresh_token_required
from smartexpenses.Model.expense import Expense
import datetime

tzx = datetime.timezone(datetime.timedelta(hours=1))
d = datetime.datetime.now(tz=tzx)

parser = reqparse.RequestParser()
parser.add_argument('title', help = 'This field cannot be blank', required = True)
parser.add_argument('private', help = 'This field cannot be blank', type=inputs.boolean, required = True)
parser.add_argument('currency', help = 'This field cannot be blank', required = True)
parser.add_argument('value', help = 'This field cannot be blank', required = True)
parser.add_argument('valueUSD', help = 'This field cannot be blank', required = True)
parser.add_argument('lattitude', help = 'This field cannot be blank', required = True)
parser.add_argument('longitude', help = 'This field cannot be blank', required = True)
parser.add_argument('address', help = 'This field cannot be blank', required = True)
parser.add_argument('categoryID', help = 'This field cannot be blank', required = True)
parser.add_argument('user_id', help = 'This field cannot be blank', required = True)

class AllExpenses(Resource):
    @jwt_refresh_token_required
    def get(self):
        try:
            return Expense.return_all()
        except Exception as error:
            return { 
                'message': repr(error),
                'status' : 1
            }, 500

    @jwt_refresh_token_required
    def delete(self):
        return {'message': 'Delete all expenses'}
    
class ReturnImages(Resource):
    @jwt_refresh_token_required
    def get(self):
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
            }
        ] 
        return allImageUrl

class GetExpenseById(Resource):
    @jwt_refresh_token_required
    def get(self,id):
        try:
            return Expense.find_by_id(id)
        except Exception as error:
            return {
                'message':repr(error),
                'status':1
            }, 500
        

class AddExpense(Resource):
    @jwt_refresh_token_required
    def post(self):
        data = parser.parse_args()
        new_expense = Expense(
            title = data['title'],
            private = data['private'],
            currency = data['currency'],
            value = data['value'],
            valueUSD = data['valueUSD'],
            lattitude = data['lattitude'],
            longitude = data['longitude'],
            address = data['address'],
            categoryID = data['categoryID'],
            date = d.strftime('%Y-%m-%d %H:%M:%S'),
            user_id = data['user_id']
        )

        try:
            new_expense.save_to_db()           
            return { 
                'message':'Your expense {} was created'.format(data['title']),
                'status' : 0
            }, 200
        except Exception as error:
            return { 
                'message': repr(error),
                'status' : 1
            }, 500
    
    