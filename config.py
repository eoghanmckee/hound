import os, json
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    with open(os.getenv(
        'CONFIG_PATH', 'config/config.json')) as config_data:
        CONFIG = json.load(config_data)

    SECRET_KEY = CONFIG['SECRET_KEY']

    # Use for upgrading/downgrading database locally:
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{}:{}@{}:5432/{}".format(
        CONFIG['POSTGRES_USER'],
        CONFIG['POSTGRES_PASSWORD'],
        CONFIG['POSTGRES_HOST'],
        CONFIG['POSTGRES_DB'])
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    CASE_BASEURL = 'http://localhost:8080/edit/'