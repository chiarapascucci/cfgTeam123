from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
# field which will take in strings in our all_forms
from wtforms.validators import DataRequired, Length, Email, EqualTo, email_validator, ValidationError


# the validators above will ensure that the form does not accept empty fields, and allows us to
# dictate the minimum and maximum length of input into these fields, ensure that the confirm password
# field only works if its the same as the password field etc.

class RegistrationForm(FlaskForm):
    # FlaskForm inherited to give us access to all the flask_wtf features and validators etc.
    user_name = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    # form fields are all imported classes as well
    user_name = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me?')
    submit = SubmitField('Login')
