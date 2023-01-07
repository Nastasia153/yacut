from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from settings import Config

yacut = Flask(__name__)
yacut.config.from_object(Config)
db = SQLAlchemy(yacut)
migrate = Migrate(yacut, db)

from . import error_handlers, views, api_views
