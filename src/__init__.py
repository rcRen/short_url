from flask import Flask
from src.config import config, db
from src.views import api


def create_app(config_mode):
    app = Flask(__name__)
    app.config.from_object(config[config_mode])
    app.static_folder = 'static'
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.register_blueprint(api, url_prefix="/api")

    return app
