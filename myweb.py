from flask import Flask
apl = Flask(__name__)

@apl.route('/')
def index():
	return '<h1>Hello,World!</h1>'

@apl.route('/user/<name>')
def user(name):
	return '<h1>Hello, %s</h1>' %name

if __name__ == '__main__':
	apl.run(debug=True)
