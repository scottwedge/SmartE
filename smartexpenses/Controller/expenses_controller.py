from flask_restful import Resource, reqparse, inputs
from binascii import hexlify
from flask_jwt_extended import jwt_refresh_token_required,get_jwt_identity
from smartexpenses.Model.expense import Expense
from smartexpenses.Model.user import User
from smartexpenses.Model.profile import Profile

parser = reqparse.RequestParser()
parser.add_argument('title', help = 'This field cannot be blank', required = True)
parser.add_argument('private', help = 'This field cannot be blank', type=inputs.boolean, required = True)
parser.add_argument('currency', help = 'This field cannot be blank', required = True)
parser.add_argument('value', help = 'This field cannot be blank', required = True)
parser.add_argument('latitude')
parser.add_argument('longitude')
parser.add_argument('address')
parser.add_argument('categoryID', help = 'This field cannot be blank', required = True)

class AllExpenses(Resource):
    @jwt_refresh_token_required
    def get(self):
        token_email = get_jwt_identity()
        user_id = User.find_by_email(token_email).id
        try:
            return {
                'expenses' : Expense.return_all_by_user_id(user_id),
                'status' : 0
            }
        except Exception as error:
            return { 
                'message': repr(error),
                'status' : 1
            }, 500

    @jwt_refresh_token_required
    def delete(self):
        return {'message': 'Delete all expenses'}

class AdminAllExpenses(Resource):
    @jwt_refresh_token_required
    def get(self):
        token_email = get_jwt_identity()
        user_id = User.find_by_email(token_email).id
        UserIsAdmin = Expense.isAdmin(user_id)
        print(UserIsAdmin)
        try:
            if UserIsAdmin:
                return {
                    'expenses' : Expense.return_all(),
                    'status' : 0
                }
            else:
               return {
                    'message' : 'sorry, you are not the administrator',
                    'status' : 1
                } 
        except Exception as error:
            return { 
                'message': repr(error),
                'status' : 1
            }, 500

class GetExpense(Resource):
    @jwt_refresh_token_required
    def get(self, expense_id):
        token_email = get_jwt_identity()
        user_id = User.find_by_email(token_email).id
        try:
            return {
                'expenses' : Expense.find_by_userid_and_expenseid(user_id, expense_id),
                'status' : 0
            }
        except Exception as error:
            return {
                'message': repr(error),
                'status' : 1
            }, 500
        
class GetRecentExpenses(Resource):
    @jwt_refresh_token_required   
    def get(self, number):
        token_email = get_jwt_identity()
        user_id = User.find_by_email(token_email).id
        try:
            return {
                'expenses' : Expense.find_recents_by_user_id(number, user_id),
                'status' : 0
            }
        except Exception as error:
            return{
                'message' : repr(error),
                'status': 1
            }, 500

class AddExpense(Resource):
    @jwt_refresh_token_required   
    def post(self):
        token_email = get_jwt_identity()
        user_id = User.find_by_email(token_email).id
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
            date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            user_id = user_id
        )
        try:
            new_expense.refresh_record_in_db()
            user_ids = new_expense.user_id
            Profile.find_by_user_id(user_ids)         
            return { 
                'expense' : Expense.find_by_userid_and_expenseid(user_id, new_expense.id),
                'message':'Your expense {} was created'.format(data['title']),
                'status' : 0
            }, 200
        except Exception as error:
            return { 
                'message': repr(error),
                'status' : 1
            }, 500
    
class UpdateExpense(Resource):
   @jwt_refresh_token_required
   def put(self, id):
        token_email = get_jwt_identity()
        user_id = User.find_by_email(token_email).id
        expense = Expense.find_by_user_id(user_id)
        data = parser.parse_args()
        value_usd = '%.2f'%(int(data['value'])/300)

        expense.title = data['title']
        expense.private = data['private']
        expense.currency = data['currency']
        expense.value = data['value']
        expense.valueUSD = value_usd
        expense.latitude = data['latitude']
        expense.longitude = data['longitude']
        expense.address = data['address']
        expense.categoryID = data['categoryID']
        expense.date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        expense.user_id = user_id

        try:
            Expense.update_to_db()           
            return { 
                'message':'Your expense {} was updated'.format(data['title']),
                'status' : 0
            }, 200
        except Exception as error:
            return { 
                'message': repr(error),
                'status' : 1
            }, 500

class DeleteExpense(Resource):
    @jwt_refresh_token_required   
    def delete(self, expense_id):
        token_email = get_jwt_identity()
        user_id = User.find_by_email(token_email).id
        try:           
            return{
                'message':Expense.delete_by_user_id(user_id, expense_id),
                'status':0
            },200
        except Exception as error:
            return {
                'message':repr(error),
                'status':1
            }, 500
        

class GetExpenseLocation(Resource):
    @jwt_refresh_token_required
    def get(self):
        token_email = get_jwt_identity()
        user_id = User.find_by_email(token_email).id
        try:
            
            return{
                'location': Expense.get_expense_location(user_id),
                'status':0
            }
        except Exception as error:
            return{
                'message':repr(error),
                'status':1
            },500

