import os
import secrets
from app import mail
from flask import url_for, current_app
from PIL import Image
from flask_mail import Message

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