from app import db,m_login
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer
from flask import current_app

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),  nullable=False)
    email = db.Column(db.String(120), nullable=False)
    picture = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)  #Post:class name

    @staticmethod
    def __repr__(self):
        return f"User details: \n Id: {self.id} \n Username: {self.username} \n Email: {self.email}" \
               f" \n Image file: {self.picture} \n"

@m_login.user_loader
def uload(uid):
    return User.query.get(int(uid))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    postdate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)   #user:name of db column
    def __repr__(self):
        return f"Post details: \n Id: {self.id} \n Title: {self.title} \n Date Posted: " \
               f"{self.date_posted} \n Content: {self.content} \n"
