from flask import request, jsonify
from smartexpenses import app, languages

@app.route('/', methods=['GET'])
def test():
    return jsonify({'message ' : 'It works!'})

@app.route('/lang', methods=['GET'])
def returnAll():
    return jsonify({'languages' : languages})

@app.route('/lang/<string:name>', methods=['GET'])
def returnOne(name):
    langs = [language for language in languages if language['name'] == name]
    return jsonify({'language ' : langs[0]})