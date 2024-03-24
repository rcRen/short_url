from flask import Flask
from flask_cors import CORS
from src.routes import api
from src.connection import setup_connection, load_config


def create_app():
    app = Flask(__name__)
    CORS(app)
    Config = load_config()
    app.config.from_object(Config)
    app.static_folder = 'static'

    with app.app_context():
        app.cassandra_session = setup_connection(Config)

    app.register_blueprint(api, url_prefix="/api")

    return app
