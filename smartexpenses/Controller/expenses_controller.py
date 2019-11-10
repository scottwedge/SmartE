from flask_restful import Resource, reqparse, inputs
from binascii import hexlify
from flask_jwt_extended import jwt_refresh_token_required,get_jwt_identity
import jwt
from smartexpenses.Model.expense import Expense
import datetime

tzx = datetime.timezone(datetime.timedelta(hours=1))
d = datetime.datetime.now(tz=tzx)

parser = reqparse.RequestParser()
parser.add_argument('title', help = 'This field cannot be blank', required = True)
parser.add_argument('private', help = 'This field cannot be blank', type=inputs.boolean, required = True)
parser.add_argument('currency', help = 'This field cannot be blank', required = True)
parser.add_argument('value', help = 'This field cannot be blank', required = True)
parser.add_argument('latitude', help = 'This field cannot be blank', required = True)
parser.add_argument('longitude', help = 'This field cannot be blank', required = True)
parser.add_argument('address', help = 'This field cannot be blank', required = True)
parser.add_argument('categoryID', help = 'This field cannot be blank', required = True)

class AllExpenses(Resource):
    @jwt_refresh_token_required
    
    def get(self):
        # get curentId
        token_email = get_jwt_identity()
        currentId = Expense.find_id_by_email(token_email)
        try:
            return Expense.return_all(currentId)
        except Exception as error:
            return { 
                'message': repr(error),
                'status' : 1
            }, 500

    @jwt_refresh_token_required
    def delete(self):
        return {'message': 'Delete all expenses'}
    

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
        
class GetRecentExpense(Resource):
    @jwt_refresh_token_required   
    def get(self,number):
        token_email = get_jwt_identity()
        currentId = Expense.find_id_by_email(token_email)
        try:
            return Expense.recent_expense(number,currentId)
        except Exception as error:
            return{
                'message':repr(error),
                'status':1
            },500


class AddExpense(Resource):
    @jwt_refresh_token_required   
    def post(self):
        token_email = get_jwt_identity()
        currentId = Expense.find_id_by_email(token_email)
        data = parser.parse_args()
        value_usd = '%.2f'%(int(data['value'])/300)
        new_expense = Expense(
            title = data['title'],
            private = data['private'],
            currency = data['currency'],
            value = data['value'],
            valueUSD = value_usd,
            latitude = data['latitude'],
            longitude = data['longitude'],
            address = data['address'],
            categoryID = data['categoryID'],
            date = d.strftime('%Y-%m-%d %H:%M:%S'),
            user_id = currentId
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
    

class UpdateExpenseById(Resource):
   @jwt_refresh_token_required
   def put(self,id):
        update_expense = Expense.find_by_id(id)
        print(update_expense)
        token_email = get_jwt_identity()
        currentId = Expense.find_id_by_email(token_email)
        data = parser.parse_args()
        value_usd = '%.2f'%(int(data['value'])/300)
        new_expense=[{
            'id':id,
            'title':data['title'],
            'private':data['private'],
            'currency': data['currency'],
            'value':data['value'],
            'valueUSD':value_usd,
            'latitude':data['latitude'],
            'longitude':data['longitude'],
            'address':data['address'],
            'categoryID':data['categoryID'],
            'date':d.strftime('%Y-%m-%d %H:%M:%S'),
            'user_id':currentId
        }]   
        try:
            Expense.update_to_db(new_expense)           
            return { 
                'message':'Your expense {} was updated'.format(data['title']),
                'status' : 0
            }, 200
        except Exception as error:
            return { 
                'message': repr(error),
                'status' : 1
            }, 500


class DeleteExpenseById(Resource):
    @jwt_refresh_token_required   
    def delete(self,id):
        try:
            Expense.delete_by_id(id)
            return{
                'message':'success delete expense',
                'status':0
            },200
        except Exception as error:
            return {
                'message':repr(error),
                'status':1
            }, 500
        
