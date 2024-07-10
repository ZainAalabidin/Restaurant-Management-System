#config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('RMS_MYSQL_USER')}:{os.getenv('RMS_MYSQL_PWD')}@"
        f"{os.getenv('RMS_MYSQL_HOST')}/{os.getenv('RMS_MYSQL_DB')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')
    DEFAULT_IMAGE = os.environ.get('DEFAULT_IMAGE')