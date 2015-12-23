from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from config import config
from flask.ext.login import LoginManager
from flask.ext.pagedown import PageDown


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
	apl = Flask(__name__)
	apl.config.from_object(config[config_name])
	config[config_name].init_app(apl)

	bootstrap.init_app(apl)
	mail.init_app(apl)
	moment.init_app(apl)
	db.init_app(apl)
	login_manager.init_app(apl)
	pagedown.init_app(apl)

	from .main import main as main_blueprint
	apl.register_blueprint(main_blueprint)

	from .auth import auth as auth_blueprint
	apl.register_blueprint(auth_blueprint, url_prefix = '/auth')


	return apl


