import os
import secrets
from app import mail
from flask import url_for, current_app
from PIL import Image
from flask_mail import Message

def edit_background(username,avater):
    random = secrets.token_hex(8)
    _, fn_ext = os.path.split(avater.filename)
    picturename = random + '-' + username + fn_ext
    img = Image.open(avater)
    output_size = (125,125)
    img.thumbnail(output_size)
    path = os.path.join(current_app.root_path, f'static/picture/{picturename}')
    img.save(path)

    return picturename

def edit_picture(username,avater):
    random = secrets.token_hex(8)
    _, fn_ext = os.path.split(avater.filename)
    picturename = username + '-' + random + fn_ext
    img = Image.open(avater)
    output_size = (125,125)
    img.thumbnail(output_size)
    path = os.path.join(current_app.root_path, f'static/picture/{picturename}')
    img.save(path)

    return picturename

def reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request",
                  sender="2631568300@qq.com",
                  recipients=[f"{user.email}"])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)