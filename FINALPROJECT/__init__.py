from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = '1851c6857d5faef882b989422f9d3165'

# how to generate secret key
# (venv) C:\Users\akhan\PycharmProjects\cfgTeam123>python
# Python 3.9.9 (tags/v3.9.9:ccb0e6a, Nov 15 2021, 18:08:50) [MSC v.1929 64 bit (AMD64)] on win32
# Type "help", "copyright", "credits" or "license" for more information.
# >>> import secrets
# >>> secrets.token_hex(16)
# '1851c6857d5faef882b989422f9d3165'
# >>>

from FINALPROJECT import routes
