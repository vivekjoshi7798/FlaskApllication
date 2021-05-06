import os.path
import secrets
from PIL import Image
from flask import url_for,current_app
from BlogApplication import mail
from flask_mail import Message


def save_Picture(temp_pic):
    random_hax = secrets.token_hex(8)
    abc, ext = os.path.splitext(temp_pic.filename)
    pic_name = random_hax + ext
    try:
        picture_path = os.path.join(current_app.root_path, 'static/profile_pic', pic_name)
    except FileNotFoundError:
        picture_path=None
    # print(ext,'\n',temp_pic.filename,'\n',picture_path,'\n',pic_name,'\n',current_app.root_path)
    outputsize = (125, 125)
    i = Image.open(temp_pic)
    i.thumbnail(outputsize)
    i.save(picture_path)

    # print(ext,'\n',temp_pic.filename,'\n',picture_path,'\n',pic_name,'\n',current_app.root_path)
    return pic_name


def sendMail(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
    {url_for('users.reset_token', token=token, _external=True)}
    If you did not make this request then simply ignore this email and no changes will be made.
    '''
    print(user.email)
    mail.send(msg)
