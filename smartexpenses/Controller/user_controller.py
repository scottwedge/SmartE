from flask import Blueprint, request, abort, make_response, jsonify
from smartexpenses.Model.user import User

user_routes = Blueprint('user_controller', __name__)

@user_routes.route('/user', methods=['GET'])
def returnAll():
    users = User.query.all()
    return jsonify({'users': users}), 201

@user_routes.route('/user/<user_id>', methods=['GET'])
def returnOne(user_id):
    users = [user for user in users if language['id'] == user_id]
    if not users:
        abort(404)
    return jsonify({'user ' : users[0]})

@user_routes.route('/user', methods=['POST'])
def create_user():
    if not request.json or not 'username' in request.json:
        abort(400)
    user = {
        'username' : request.json['username']
    }
    User.add(user)
    return jsonify({'user': user}), 201

@user_routes.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
