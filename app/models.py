from app import db,m_login
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Sl
from flask import current_app,url_for
from markdown import markdown
import bleach
class ValidationError(ValueError):
    pass
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    postid = db.Column(db.Integer, db.ForeignKey('post.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
                        'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

db.event.listen(Comment.body, 'set', Comment.on_changed_body)

class Follow(db.Model):
    __tablename__='follows'
    followerid=db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True)
    followedid=db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True)
    timestamp=db.Column(db.DateTime,default=datetime.utcnow())
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),  nullable=False)
    email = db.Column(db.String(120), nullable=False)
    picture = db.Column(db.String(20), nullable=False, default='default.png')
    background=db.Column(db.String(30),default='defaultbackground.png')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)  #Post:class name
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    followed = db.relationship('Follow',
                               foreign_keys=[Follow.followerid],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follow',
                                foreign_keys=[Follow.followedid],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')

    def get_reset_token(self, expires_sec=1800):
        s = Sl(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id})
    @staticmethod
    def verify_reset_token(token):
        s =Sl(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get_or_404(user_id)
    def follow(self,user):
        if not self.is_following(user):

            f=Follow(follower=self,followed=user)
            db.session.add(f)
            db.session.commit()

    def unfollow(self, user):
        f = self.followed.filter_by(followedid=user.id).first()
        if f:
            db.session.delete(f)
            db.session.commit()

    def is_following(self,user):
        return self.followed.filter_by(followedid=user.id).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(
            followerid=user.id).first() is not None


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

    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    def __repr__(self):
        return f"Post details: \n Id: {self.id} \n Title: {self.title} \n Date Posted: " \
               f"{self.date_posted} \n Content: {self.content} \n"



