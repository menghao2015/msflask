from flask import render_template,redirect,flash, url_for, request 
from flask.ext.login import login_user, current_user
from flask.ext.login import logout_user,login_required

from . import auth
from .forms import LoginForm
from .forms import RegistrationForm
from ..models import User
from .. import db
from ..email  import send_email

@auth.route('/login', methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash('invalid user or password')
	return render_template('auth/login.html',form = form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('you have been logged out.')
	return redirect(url_for('main.index'))	

@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(email = form.email.data,
					username = form.username.data,
					password = form.password.data)
		db.session.add(user)
		db.session.commit()
		token = user.generate_confirmation_token()
		send_email(user.email, 'accunt confirmed',
				'auth/email/confirm', user = user, token = token)
		flash('A confirmation email has been sent to your email.')
		return redirect(url_for('main.index'))
	return render_template('auth/register.html', form = form )

@auth.route('/confirm')
@login_required
def resend_confirmation():
	token = user.generate_confirmation_token()
	send_email(user.email, 'accunt confirmed',
			'auth/email/confirm', user = user, token = token)
	flash('A new confirmation email has been sent to your email.')
	return redirect(url_for('main.index'))
	
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		flash(' accunt compelice')
	else:
		flash('The lick is invalid or has expired')
	return redirect(url_for('main.index'))

@auth.before_request
def before_request():
	if curent_user.is_authenticated() \
		and not current_user.confirmed \
		and request.endpoint[:5] != 'auth.':
		return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonmous() or current_user.confirmed():
		return redirect(url_for('main.index'))
	return render_template('auth/unconfirmed.html')


	


