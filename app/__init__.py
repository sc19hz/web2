from flask import Flask
from flask_mail import Mail
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_moment import Moment
from flask_bootstrap import Bootstrap
db = SQLAlchemy()
bc=Bcrypt()
m_login=LoginManager()
m_login.login_view="users.login" #function
m_login.login_message_category="info" #color
mail=Mail()
moment = Moment()

def create(config_class=Config):
    app=Flask(__name__)
    bootstrap = Bootstrap(app)
    app.config.from_object(Config)
    db.init_app(app)
    bc.init_app(app)
    m_login.init_app(app)
    mail.init_app(app)

    from app.main.views import main
    from app.users.views import users
    from app.posts.views import posts
    from app.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(posts)
    app.register_blueprint(errors)
    return app
app=create() #this is for deploying
