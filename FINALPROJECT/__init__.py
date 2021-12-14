from flask import Flask

from flask_login import LoginManager

from FINALPROJECT.config import USER, PASSWORD, HOST

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# the flask LoginManager needs to be instantiated so that we can use Flask-Login with our application, load a user from their ID and track their user session
# once it's instantiated we configure it with out application object (line 9), and use it with the user_loader callback in models.py
# the login_view allows us to specify the url which we are using to log in users (the login page in this case)


app.config['SECRET_KEY'] = config.SECRET_KEY
app.secret_key = config.SECRET_KEY

# CSRF token (cross site request forgery) - secret key will help prevent hacking of forms and information entered into them in conjunction
# with the forms.hidden_tag() function in implemented on the login and registration forms


from FINALPROJECT import routes
