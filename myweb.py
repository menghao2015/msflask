from flask import Flask, render_template, make_response, session,redirect, url_for, flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from datetime import datetime
from flask.ext.moment import Moment

from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

from flask.ext.sqlalchemy import SQLAlchemy

apl = Flask(__name__)
apl.config['SECRET_KEY'] = 'hard to guess string'
apl.config['SQLACHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/data_dev'
apl.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(apl)
apl_manager = Manager(apl)
bootstrap = Bootstrap(apl)
moment = Moment(apl)

class NameForm(Form):
	name = StringField('What is your name?', validators=[Required()])
	submit = SubmitField('Summit')

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	users = db.relationship('User', backref='role')

	def __repr__(self):
		return '<Role %r>' % self.name

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

	def __repr__(self):
		return '<User %r>' % self.username









@apl.route('/',methods=['GET','POST'])
def index():
	name = None
	form = NameForm()
	if form.validate_on_submit():
		old_name = session.get('name')
		if old_name is not None and old_name != form.name.data:
			flash('Looks like you have changed your name!')
		session['name'] = form.name.data
		return redirect(url_for('index'))
	return render_template('index.html',form=form, name=session.get('name'), current_time=datetime.utcnow())

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
