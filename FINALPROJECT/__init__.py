from flask import Flask
import mysql.connector
from typing import List

from flask_login import LoginManager

from FINALPROJECT.config import USER, PASSWORD, HOST

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

"""
https://hackersandslackers.com/configure-flask-applications/
above is link with info about app.config for when you want to encrypt information i think
"""

app.config['SECRET_KEY'] = config.SECRET_KEY
app.secret_key = config.SECRET_KEY

# how to generate secret key
# (venv) C:\Users\akhan\PycharmProjects\cfgTeam123>python
# Python 3.9.9 (tags/v3.9.9:ccb0e6a, Nov 15 2021, 18:08:50) [MSC v.1929 64 bit (AMD64)] on win32
# Type "help", "copyright", "credits" or "license" for more information.
# >>> import secrets
# >>> secrets.token_hex(16)
# '1851c6857d5faef882b989422f9d3165'
# >>>

from FINALPROJECT import routes
