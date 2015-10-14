from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User



class ChangeEmailForm(Form):
	email = StringField('email', validators= [Required(), Length(1,64), Email()])
	submit = SubmitField('submit')

class CheckEmailForm(Form):
	email = StringField('your email', validators = [Required(), Length(1,64), Email()])
	submit = SubmitField('submit')

class ResetPasswordForm(Form):
	email = StringField('email', validators=[Required(), Length(1,64), Email()])
	new_password1 = PasswordField('new password', validators = [Required(), 
								EqualTo('new_password2', 'password do not match')])

	new_password2 = PasswordField('confirm password', validators = [Required()])
	submit = SubmitField('submit')
	
	def validate_email(self,field):
		if User.query.filter_by(email = field.data).first() is None:
			raise  ValidationError('Unknown email')


class ChangePasswordForm(Form):
	old_password = PasswordField('old_password', validators = [Required()])
	new_password1 = PasswordField('NewPassword', validators = [Required(),
					 EqualTo('new_password2', 'PW do not match')])

	new_password2 = PasswordField('confirm password', validators = [Required()])
	submit = SubmitField('submit')

class LoginForm(Form):
	email = StringField('email', validators = [Required(),
					 Length(1,64),Email()])
	password = PasswordField('password', validators = [Required()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Log in ')


class RegistrationForm(Form):
	email = StringField('email', validators=[Required(),Length(1,64), Email()])
	username = StringField('username', validators=[Required(), Length(1,64),
						Regexp('^[A-Za-z][A-Za-z0-9._]*$',0,
						'Username must have only letters,numbers, dots or underscores')])
	password = PasswordField('password',validators=[Required(), EqualTo('password2', 'password do not match')])
	password2 = PasswordField('confirm password', validators = [Required()])
	submit = SubmitField('register')

	def validate_email(self,field):
		if User.query.filter_by(email = field.data).first():
			raise ValidationError('email already  registered.')

	def validate_username(self,field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already in use.')



