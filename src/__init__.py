from flask import Flask
from flask_cors import CORS
from src.config import config, db
from src.views import api
from src.models.db_connect import connect_to_cassandra


def create_app(config_mode):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config[config_mode])
    app.static_folder = 'static'

    with app.app_context():
        app.cassandra_session = connect_to_cassandra(config_mode)

    app.register_blueprint(api, url_prefix="/api")

    return app
