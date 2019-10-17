from flask import Blueprint, request, jsonify

root = Blueprint('root', __name__)

languages = [
    {'name' : 'JavaScript'},
    {'name' : 'Python'},
    {'name' : 'Ruby'}
]

@root.route('/', methods=['GET'])
def test():
    return jsonify({'message ' : 'It works!'})

@root.route('/lang', methods=['GET'])
def returnAll():
    return jsonify({'languages' : languages})

@root.route('/lang/<string:name>', methods=['GET'])
def returnOne(name):
    langs = [language for language in languages if language['name'] == name]
    return jsonify({'language ' : langs[0]})