from flask_restful import Resource, reqparse, inputs
from binascii import hexlify
from smartexpenses.Model.expense import Expense

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
parser.add_argument('date', help = 'This field cannot be blank', required = True)
parser.add_argument('user_id', help = 'This field cannot be blank', required = True)

class AllExpenses(Resource):
    def get(self):
        return Expense.return_all()

    def delete(self):
        return {'message': 'Delete all expenses'}

class GetExpenseById(Resource):
    def get(self):
        return {'message': 'return some message'}


class AddExpenses(Resource):
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
            date = data['date'],
            user_id = data['user_id']
        )

        try:
            new_expense.save_to_db()
            return{ 'message':'Your expense {} was created'.format(data['title'])},200
        except:
            return {'message': 'Something went wrong'}, 500
    
    