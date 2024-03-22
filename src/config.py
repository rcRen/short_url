import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))


load_dotenv()

db = SQLAlchemy()


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    CASSANDRA_KEYSPACE = 'links'
    CASSANDRA_HOST = os.environ.get('CASSANDRA_DEVELOPMENT_HOST',"localhost")
    CASSANDRA_PORT = int(os.environ.get('CASSANDRA_DEVELOPMENT_PORT',"9042"))
    CQLENG_ALLOW_SCHEMA_MANAGEMENT = 'CQLENG_ALLOW_SCHEMA_MANAGEMENT'

    # SQLALCHEMY_DATABASE_URI = os.getenv('DEVELOPMENT_DATABASE_URL')


class ProductionConfig(Config):
    CASSANDRA_KEYSPACE = 'links'
    CASSANDRA_HOSTS = os.environ.get('CASSANDRA_PRODUCTION_HOST')
    CQLENG_ALLOW_SCHEMA_MANAGEMENT = 'CQLENG_ALLOW_SCHEMA_MANAGEMENT'


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
