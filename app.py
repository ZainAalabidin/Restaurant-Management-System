from flask import Flask
from flask_migrate import Migrate
from models import User
from extensions import db, bcrypt, login_manager
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def create_app():
    """
    Create and configure the Flask application.

    Returns:
        app (Flask): The Flask application instance.
    """
    app = Flask(__name__, template_folder="templates", static_folder="static")
    
    # Load configuration from config.py
    app.config.from_object("config.Config")

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Set the login view and message category for Flask-Login
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    # Register application routes
    from routes import register_routes
    register_routes(app, db, bcrypt)

    # Set up database migration
    migrate = Migrate(app, db)

    return app


@login_manager.user_loader
def load_user(user_id):
    """
    Load a user from the database by their user ID.

    Args:
        user_id (int): The ID of the user to load.

    Returns:
        User: The user instance if found, otherwise None.
    """
    return User.query.get(int(user_id))
