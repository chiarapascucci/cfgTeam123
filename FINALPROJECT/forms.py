import mysql
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
# field which will take in strings in our all_forms
from wtforms.validators import DataRequired, Length, Email, EqualTo, email_validator, ValidationError


class RegistrationForm(FlaskForm):
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

# need to set a secret key for our application, a secret key will protect against modifying cookies and forgery
# attacks