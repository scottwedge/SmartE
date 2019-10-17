from flask import Flask

app = Flask(__name__)

languages = [
    {'name' : 'JavaScript'},
    {'name' : 'Python'},
    {'name' : 'Ruby'}
]

if __name__ == "__main__":
    app.run(debug=True)
