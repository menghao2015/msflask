from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email

class LoginForm(Form):
	email = StringField('email', validators = [Required(),
					 Length(1,64),Email()])
	password = PasswordField('password', validators = [Required()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Log in ')
