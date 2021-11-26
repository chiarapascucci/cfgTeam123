from flask import Flask, render_template, url_for, flash, redirect
from FINALPROJECT import app
from FINALPROJECT.forms import RegistrationForm, LoginForm
# from flask_bcrypt import Bcrypt
from FINALPROJECT.test_db_functions import create_user_in_db, validate_user
from wtforms import validators


# bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('home.html', title='home')


@app.route('/tester')
def tester():
    return render_template('tester.html', title='tester')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        create_user_in_db(form.user_name.data, form.first_name.data, form.last_name.data, form.password.data)
        flash(f'Account created for {form.user_name.data}!', 'Success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        validate_user(form.user_name.data, form.password.data)
        flash('You have been logged in', 'success')
        return redirect(url_for('home'))
    else:
        flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='login', form=form)


@app.route('/browsegames')
def browsegames():
    return render_template('browsegames.html', title='browsegames')
