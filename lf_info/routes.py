from flask import Blueprint, render_template, send_from_directory

from .data.info import Info
from .data.web_texts import WebTexts

bp = Blueprint("main", __name__)


def setup_routes(app):
    app.register_blueprint(bp)


@bp.route("/")
def index():
    return render_template("activities_reload.html")


@bp.route("/activity_list")
def activity_list():
    info = Info()
    activities = info.get_classes_list_for_web_page()
    return render_template("activity_list.html", activities=activities)


@bp.route("/activities-reload")
def activities_reload():
    return render_template("activities_reload.html")


@bp.route("/images/<filename>")
def images(filename):
    return send_from_directory("static/images", filename)


@bp.route("/css/<filename>")
def styles(filename):
    return send_from_directory("static/css", filename)


@bp.route("/ticker")
def ticker():
    ticker_items = WebTexts().get_ticker_texts_ticker()
    # Add a couple of long blank line to the ticker items
    ticker_items.append(" " * 60000)
    ticker_items.append(" " * 60000)
    ticker_items.append(" " * 60000 + "*")
    return render_template("ticker.html", ticker_items=ticker_items)
