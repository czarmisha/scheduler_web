import secrets
import os, config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
# from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config.from_object('config.DevelopementConfig')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'

from . import views
