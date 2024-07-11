from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__)


@home_bp.route("/")
@home_bp.route("/home")
def home():
    return render_template("home.html", restaurant_name="YummYum")
@home_bp.route("/about")
def about():
    return render_template("about.html", restaurant_name="YummYum")