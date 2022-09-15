import os
from dotenv import load_dotenv

app_dir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

db_host = os.environ['POSTGRES_HOST']
db_username = os.environ['POSTGRES_USERNAME']
db_password = os.environ['POSTGRES_PASSWORD']
db_name = os.environ['POSTGRES_DB']
    

class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopementConfig(BaseConfig):
    DEBUG = True
    BOT_TOKEN=os.environ['BOT_TOKEN']
    BOT_USERNAME=os.environ['BOT_USERNAME']
    BOT_AUTH_REDIRECT=os.environ['BOT_AUTH_REDIRECT']
    SQLALCHEMY_DATABASE_URI = f'postgresql://{db_username}:{db_password}@{db_host}:5432/{db_name}'


class TestingConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass