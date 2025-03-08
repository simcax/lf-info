from flask import Flask

from .routes import setup_routes


def create_app():
    app = Flask(__name__)
    app.config["SECRET"] = "dev"
    app.config["SERVER_NAME"] = "localhost"
    app.config["APPLICATION_ROOT"] = "/"
    app.config["PREFERRED_URL_SCHEME"] = "https"
    setup_routes(app)
    return app
