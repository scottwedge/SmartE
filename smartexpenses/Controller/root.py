from flask import Blueprint, request, abort, make_response, jsonify

root = Blueprint('root', __name__)

@root.route('/', methods=['GET'])
def landing():
    return jsonify({'message ' : 'It works!'})