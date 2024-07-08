from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from models import User
from extensions import db
from dotenv import load_dotenv
import os

bcrypt = Bcrypt()
login_manager = LoginManager()



def create_app():
    load_dotenv()
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{os.getenv('RMS_MYSQL_USER')}:{os.getenv('RMS_MYSQL_PWD')}@"
        f"{os.getenv('RMS_MYSQL_HOST')}/{os.getenv('RMS_MYSQL_DB')}"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config['UPLOAD_FOLDER'] = '/home/zain/Restaurant-Management-System/static/images/'
    app.config['DEFAULT_IMAGE'] = 'default.png'

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'


    from routes import register_routes

    register_routes(app, db)
    migrate = Migrate(app, db)

    from routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))