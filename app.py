#app.py
from flask import Flask
from flask_migrate import Migrate
from models import User
from extensions import db, bcrypt, login_manager
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    # Load configuration from config.py
    app.config.from_object('config.Config')

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    from routes import register_routes
    register_routes(app, db, bcrypt)

    migrate = Migrate(app, db)

    return app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))