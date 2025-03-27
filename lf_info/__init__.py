import os
import re

import sentry_sdk
from flask import Flask
from flask_cors import CORS

from .routes import setup_routes

app_environment = os.environ.get("ENVIRONMENT_NAME", "development")

sentry_sdk.init(
    dsn="https://a788df580e7cdc6711aa4b7a6d48e786@o4505902934130688.ingest.us.sentry.io/4508949981691904",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
    environment=app_environment,
    traces_sample_rate=1.0,
)

# List of allowed origins
origins = os.environ.get("ALLOWED_ORIGINS")
# Convert comma-separated string to list
# Define regex for allowed origins (local dev and PR URLs)
env_origins_pattern = os.environ.get("ALLOWED_ORIGINS_PATTERN", "")
origins_pattern = re.compile(env_origins_pattern)
allowed_origins = origins.split(",") if origins else []


def create_app():
    app = Flask(__name__)
    CORS(app, origins=origins_pattern)
    app.config["SECRET"] = "dev"
    app.config["SERVER_NAME"] = "localhost"
    app.config["APPLICATION_ROOT"] = "/"
    app.config["PREFERRED_URL_SCHEME"] = "https"
    if app_environment == "development":
        app.config["DEBUG"] = True
        app.config["TESTING"] = True
    setup_routes(app)
    return app
