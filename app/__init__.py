import datetime
from config import Config
from flask import Flask, render_template, request, current_app, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from werkzeug.exceptions import HTTPException


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()


def create_app(cfg):
	application = Flask(__name__)
	application.config.from_object(cfg)

	init_app(application)
	db.init_app(application)
	migrate.init_app(application, db)

	login.init_app(application)
	login.login_view = 'main.login'
	
	register_blueprints(application)

	setup_jinja(application)

	return application


def register_blueprints(application):
	from app.routes import blueprint as main_blueprint

	application.register_blueprint(main_blueprint)

	return application


def setup_jinja(application):
	application.jinja_env.filters.update(

	)
	
	from app.util.icon import load_icons
	application.jinja_env.globals.update(
		ICONS=load_icons()
	)


def init_app(app):
	@app.context_processor
	def inject_variables():
		return {
			'now': datetime.datetime.utcnow()
		}

	@app.errorhandler(HTTPException)
	def handle_exception(e):
		return render_template('error.html.j2', error=e)	

	@app.after_request
	def after_request(response):
		return response


from app.models import *
