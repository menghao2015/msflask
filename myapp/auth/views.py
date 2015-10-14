from flask import render_template,redirect,flash, url_for, request 
from flask.ext.login import login_user, current_user
from flask.ext.login import logout_user,login_required

from . import auth
from .forms import LoginForm
from .forms import RegistrationForm
from .forms import ChangePasswordForm
from .forms import CheckEmailForm
from .forms import ResetPasswordForm

from ..models import User
from .. import db
from ..email  import send_email

@auth.before_app_request
def before_request():
	if current_user.is_authenticated \
			and not current_user.confirmed \
			and request.endpoint[:5] != 'auth.' \
			and request.endpoint != 'static':
		return redirect(url_for('auth.unconfirmed'))

@auth.route('/reset_password',methods = ['GET', 'POST'])
def check_email():
	form = CheckEmailForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		if user:
			token = user.generate_reset_token()
			send_email(form.email.data,'Reset Password',
					'auth/email/reset_password', user = user, token = token)
			flash('A confirmation  email send to you inbox, follow url to reset password')
			return redirect(url_for('main.index'))
		else:
			flash('invalid email')
	return render_template('auth/check_email.html', form = form) 

@auth.route('/reset_password/<token>', methods = ['GET', 'POST'])
def password_reset(token):
	if not current_user.is_anonymous:
		return redirect(url_for('main.index'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		if user is None:
			return redirect(url_for('main.index'))
		if user.reset_password(token, form.new_password1.data):
			db.session.add(user)
			flash('reset password complete')
			return redirect(url_for('auth.login'))
	return render_template('auth/reset_password.html', form = form)



@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous  or current_user.confirmed:
		return redirect(url_for('main.index'))
	return render_template('auth/unconfirmed.html')

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
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html', form = form )

	
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


@auth.route('/confirm')
@login_required
def resend_confirmation():
	token = current_user.generate_confirmation_token()
	send_email(current_user.email, 'accunt confirmed',
			'auth/email/confirm', user = current_user, token = token)
	flash('A new confirmation email has been sent to your email.')
	return redirect(url_for('main.index'))
	
@auth.route('/change_password', methods = ['GET', 'POST'])
@login_required
def change_password():
	form = ChangePasswordForm()
	if form.validate_on_submit():
		if current_user.verify_password(form.old_password.data):
			current_user.password = form.new_password1.data
			#current_user.password(form.new_password1.data) ??????????
			db.session.add(current_user)
			flash('Change password competer')
			return redirect(url_for('auth.login'))
	return render_template('auth/change_password.html', form = form)











