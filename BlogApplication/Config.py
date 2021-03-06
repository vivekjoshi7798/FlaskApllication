import os
import json

with open('/etc/config.json') as config_files:
    config=json.load(config_files)


class Config:
    SECRET_KEY = 'ffdc7ece14fc2ad2789d1f37098e62ee'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    DOMAIN = 'gmail.com'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = config.get('MAIL_USERNAME')
    MAIL_PASSWORD = config.get('MAIL_PASSWORD')
