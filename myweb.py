from flask import Flask, render_template, make_response, session,redirect, url_for, flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from datetime import datetime
from flask.ext.moment import Moment

from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

from flask.ext.sqlalchemy import SQLAlchemy

from flask.ext.script import Shell

from flask.ext.migrate import Migrate, MigrateCommand

import os
from flask.ext.mail import Mail,Message

from threading import Thread


apl = Flask(__name__)
apl.config['SECRET_KEY'] = 'hard to guess string'
apl.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/data_dev'
apl.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

apl.config['MAIL_SERVER'] = 'smtp.163.com'
apl.config['MAIL_PORT'] = 25
apl.config['MAIL_USE_TLS'] = True
apl.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
apl.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
apl.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
apl.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <lucky__menghao@163.com>'
apl.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN') or 'menghao_92@163.com'


mail = Mail(apl)
db = SQLAlchemy(apl)
apl_manager = Manager(apl)
bootstrap = Bootstrap(apl)
moment = Moment(apl)

def send_async_email(apl, msg):
	with apl.app_context():
		mail.send(msg)


migrate = Migrate(apl,db)
apl_manager.add_command('db',MigrateCommand)

def send_email(to, subject, template, **kwargs):
	msg = Message(apl.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
				sender=apl.config['FLASKY_MAIL_SENDER'],
						recipients = [to])
	msg.body = render_template(template + '.txt', **kwargs)
	msg.html = render_template(template + '.html', **kwargs)
	thr = Thread(target=send_async_email, args=[apl,msg])
	thr.start()
	return thr	




def make_shell_context():
	return dict(apl=apl, db=db, User=User, Role=Role)
apl_manager.add_command("shell", Shell(make_context=make_shell_context))


class NameForm(Form):
	name = StringField('What is your name?', validators=[Required()])
	submit = SubmitField('Summit')

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	users = db.relationship('User', backref='role')
	users = db.relationship('User', backref='role', lazy='dynamic')

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
	form = NameForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username = form.name.data).first()
		if user is None:
			user = User(username = form.name.data)
			db.session.add(user)
			session['known'] = False
			if apl.config['FLASKY_ADMIN']:
				send_email(apl.config['FLASKY_ADMIN'], 'New User',  
							'mail/new_user', user=user)
		else:
			session['known'] = True
		session['name'] = form.name.data
		return redirect(url_for('index'))
	return render_template('index.html',form=form, name=session.get('name'),\
			known = session.get('known',False), current_time=datetime.utcnow())

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
	db.create_all()
	db.session.commit()
	apl_manager.run()
