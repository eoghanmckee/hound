import logging
import os

from logging.handlers import RotatingFileHandler
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from config import Config
from apscheduler.schedulers.background import BackgroundScheduler

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = ('')
bootstrap = Bootstrap()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    app.logger.setLevel(logging.INFO)

    return app

from app import models
from runner import Runner

def runner1hour():
    Runner().iocanalysis(1)

def runner24hour():
    Runner().iocanalysis(24)

# init BackgroundScheduler job - run every 1 hour
scheduler1hour = BackgroundScheduler()
scheduler1hour.add_job(runner1hour, trigger='interval', hours=1)
scheduler1hour.start()

# init BackgroundScheduler job - run every 24 hour
scheduler24hour = BackgroundScheduler()
scheduler24hour.add_job(runner24hour, trigger='interval', hours=24)
scheduler24hour.start()