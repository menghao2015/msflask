from flask import Flask, render_template, make_response
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap


apl = Flask(__name__)
apl_manager = Manager(apl)
bootstrap = Bootstrap(apl)

@apl.route('/')
def index():
	return render_template('index.html')

@apl.route('/user/<name>')
def user(name):
	return render_template('user.html', name=name)

@apl.errorhandler(404)
def page_not_found(e):
	return render_template('404.html')

@apl.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html')





if __name__ == '__main__':
	apl_manager.run()
