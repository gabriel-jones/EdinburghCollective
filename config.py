import os
import datetime
from decouple import config


class Config(object):
	ROOT = os.path.dirname(os.path.abspath(__file__))
	APP_ROOT = os.path.join(ROOT, 'app')

	SECRET_KEY = config('SECRET_KEY')

	MAINTINENCE_MODE = config('MAINTINENCE_MODE', default=False, cast=bool)

	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_DATABASE_URI = config('DATABASE_URL')
	SQLALCHEMY_MIGRATE_REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db_repository')
	