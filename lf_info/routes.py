from flask import Blueprint, render_template

from .data.info import Info

bp = Blueprint("main", __name__)


def setup_routes(app):
    app.register_blueprint(bp)


@bp.route("/")
def index():
    return render_template("index.html", welcome_text="Welcome to Lejre Fitness Info!")


@bp.route("/activity_list")
def activity_list():
    info = Info()
    activities = info.get_classes_list_for_web_page()
    return render_template("activity_list.html", activities=activities)
