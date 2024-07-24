from flask import Blueprint, render_template

# Create a blueprint for home-related routes
home_bp = Blueprint('home', __name__)

# Route for the home page
@home_bp.route("/")
@home_bp.route("/home")
def home():
    # Render the home.html template with the restaurant name
    return render_template("home.html", restaurant_name="YummY")

# Route for the about page
@home_bp.route("/about")
def about():
    # Render the about.html template with the restaurant name
    return render_template("about.html", restaurant_name="YummY")
