from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

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
	password2 = PasswordField('conform password', validators = [Required()])
	submit = SubmitField('register')

	def validate_email(self,field):
		if User.query.filter_by(email = field.data).first():
			raise ValidationError('email already  registered.')

	def validate_username(self,field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already in use.')



