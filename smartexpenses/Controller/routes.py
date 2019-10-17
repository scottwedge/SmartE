from flask import Blueprint, request, abort, make_response, jsonify

root = Blueprint('root', __name__)

users = [
    {
        'id' : 1,
        'username' : 'Dani',
        'password' : 'apple',
        'admin' : True,
    },
    {
        'id' : 2,
        'username' : 'Joe',
        'password' : 'samsung',
        'admin' : True,
    },
    {
        'id' : 3,
        'username' : 'Maté',
        'password' : 'shitbox',
        'admin' : False,
    },
]

@root.route('/', methods=['GET'])
def test():
    return jsonify({'message ' : 'It works!'})

@root.route('/user', methods=['GET'])
def returnAll():
    return jsonify({'users' : users})

@root.route('/user/<string:user_id>', methods=['GET'])
def returnOne(user_id):
    users = [user for user in users if language['id'] == user_id]
    if not users:
        abort(404)
    return jsonify({'user ' : users[0]})

@root.route('/user', methods=['POST'])
def create_user():
    if not request.json or not 'username' in request.json:
        abort(400)
    user = {
        'username' : request.json['username']
    }
    users.append(user)
    return jsonify({'user': user}), 201

@root.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
