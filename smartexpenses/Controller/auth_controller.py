from flask_restful import Resource
from binascii import hexlify
from smartexpenses.Model.user import User

class UserRegistration(Resource):
    def post(self):
        return {'message': User registration}

class UserLogin(Resource):
    def post(self):
        return {'message': User login}

class UserLogoutAccess(Resource):
    def post(self):
        return {'message': 'User logout'}
      
      
class UserLogoutRefresh(Resource):
    def post(self):
        return {'message': 'User logout'}
      
      
class TokenRefresh(Resource):
    def post(self):
        return {'message': 'Token refresh'}
      
      
class AllUsers(Resource):
    def get(self):
        return {'message': 'List of users'}

    def delete(self):
        return {'message': 'Delete all users'}
      
      
class SecretResource(Resource):
    def get(self):
        return {
            'answer': 42
        }
      




# @user_routes.route('/signup', methods=['GET'])
# def signup():
#     if not request.json or 
#        not 'username'
#        not 'username' 
#     in request.json:
#         abort(400)
#     user = {
#         'username' : request.json['username'],
#         'email' : request.json['email'],
#         'password' : request.json['password'],
#         'admin' : 0,
#     }
#     User.add(user)
#     return jsonify({'user': user}), 201

# @user_routes.route('/signup', methods=['POST'])
# def login():
#     key = hexlify(os.urandom(length))
#     user = {
#         'username' : request.json['username'],
#         'email' : request.json['email'],
#         'password' : request.json['password'],
#         'admin' : 0,
#     }
#     User.add(user)
#     return jsonify({'user': user}), 201

# @user_routes.route('/user', methods=['GET'])
# def returnAll():
#     users = User.query.all()
#     return jsonify({'users': users}), 201

# @user_routes.route('/user/<user_id>', methods=['GET'])
# def returnOne(user_id):
#     user = User.query.get(user_id)
#     if not user:
#         abort(404)
#     return jsonify({'user ' : user})

# @user_routes.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)
