from typing import List
import mysql.connector
from flask import Flask, render_template, url_for, flash, redirect

# from all_forms.regform import RegistrationForm, LoginForm
from FINALPROJECT import app
from FINALPROJECT.config import USER, PASSWORD, HOST
from FINALPROJECT.forms import RegistrationForm, LoginForm

class DBConnectionError(Exception):
    pass


def _connect_to_db(db_name: str):
    cnx = mysql.connector.connect(host=HOST,
                                  user=USER,
                                  password=PASSWORD,
                                  auth_plugin='mysql_native_password',
                                  database='test')
    return cnx


def get_all_records() -> List:
    db_connection = None
    try:
        db_name = "test"
        db_connection = _connect_to_db(db_name)
        cursor = db_connection.cursor()
        query = "SELECT * FROM test.go_team"
        cursor.execute(query)
        result = cursor.fetchall()
        for i in result:
            print(i)
        cursor.close()

        return result

    except Exception:
        raise DBConnectionError('Failed to read the data from DB')

    finally:
        if db_connection:
            db_connection.close()
            print('DB Connection is now closed.')


"""
https://hackersandslackers.com/configure-flask-applications/
above is link with info about app.config for when you want to encrypt information i think
"""

get_all_records()


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
        flash(f'Account created for {form.username.data}!', 'Success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='login', form=form)


@app.route('/browsegames')
def browsegames():
    return render_template('browsegames.html', title='browsegames')
