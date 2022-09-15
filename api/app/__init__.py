import secrets
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate, MigrateCommand
# from flask_script import Manager, Command, Shell
# from flask_login import LoginManager
import os, config

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config.from_object('config.DevelopementConfig')

db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'

from . import views
