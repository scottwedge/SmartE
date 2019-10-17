from flask import Blueprint, request, abort, make_response, jsonify

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
    if not langs:
        abort(404)
    return jsonify({'language ' : langs[0]})

@root.route('/lang', methods=['POST'])
def create_language():
    if not request.json or not 'name' in request.json:
        abort(400)
    language = {
        'name' : request.json['name']
    }
    languages.append(language)
    return jsonify({'language': language}), 201

@root.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
