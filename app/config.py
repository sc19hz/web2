import os


class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_SERVER = 'smtp.googlemail.com'
