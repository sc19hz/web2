import os


class Config:
    SECRET_KEY = '8f25414a4e064f6b8730e2de2dcef865'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_SERVER = 'smtp.googlemail.com'
    FLASKY_POSTS_PER_PAGE = 20
    FOLLOWERS_PER_PAGE = 50