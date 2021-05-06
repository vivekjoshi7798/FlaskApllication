import os


class Config:
    SECRET_KEY = 'ffdc7ece14fc2ad2789d1f37098e62ee'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    DOMAIN = 'gmail.com'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('Email')
    MAIL_PASSWORD = os.environ.get('Pass')