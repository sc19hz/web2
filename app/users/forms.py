from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from app.models import User
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf import FlaskForm


class F_registration(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_conformation = PasswordField('Password Conformation', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def verifyname(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('The username has been used, please try another one.')
    def varifyemail(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('The email has been used, please try another one.')

class F_updateuser(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update your avatar', validators=[FileAllowed(['png', 'jpg', 'jpeg'])])
    submit = SubmitField('Update')

    def verifyname(self, username):
        if current_user.username!=username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('The username has been used, please try another one.')

    def varifyemail(self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('The email has been used, please try another one')

class F_login(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')