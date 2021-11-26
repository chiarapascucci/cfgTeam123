from FINALPROJECT import app
from FINALPROJECT.data_access_functions import create_user_in_db, validate_user, DBConnectionError, _connect_to_db
from FINALPROJECT.forms import RegistrationForm, LoginForm

from wtforms import validators
from typing import List
from flask import Flask, jsonify, request, render_template, url_for, redirect, flash
from config import USER, PASSWORD, HOST, DB_NAME
import mysql.connector
import json






"""
https://hackersandslackers.com/configure-flask-applications/
above is link with info about app.config for when you want / encrypt information i think
"""




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


@app.route('/start-timer')
def starttimer():
    return render_template('select_break_time.html', title='starttimer')


@app.route('/browsegames')
def browsegames():
    return render_template('browsegames.html', title='browsegames')

@app.route('/log-session-start', methods=['GET', 'POST'])
def logsessionstart():
    """will need some way of retrieving user ID"""
    try:
        connection = _connect_to_db(DB_NAME)
        if request.method == 'POST':

            print("post request received")

            data_dict = request.get_json()
            user_id = data_dict['user_id']
            start_time = data_dict['start_time']
            req_len = str(data_dict['requested_duration'])
            query = f"INSERT INTO {DB_NAME}.sessions (UserID, StartTime, RequestedDuration) VALUES ({user_id}, '{start_time}', {req_len});"
            print(query)
            my_cur = connection.cursor()
            my_cur.execute(query)
            my_cur.close()
            print("first cursor closed")
            follow_query = "select * from timer_test.sessions;"
            print(follow_query)
            other_cur = connection.cursor()
            other_cur.execute(follow_query)
            result = other_cur.fetchall()
            print("printing result: ", result)
            result = jsonify(result)
            print("result after jsonify: \n", result)
            other_cur.close()
            connection.close()
            print("connection closed")
            return result

    except DBConnectionError:
        print("db connection failed")


@app.route('/log-session-end', methods=['GET', 'POST'])
def logsessionend():
    try:
        connection = _connect_to_db(DB_NAME)
        if request.method == 'POST':
            print("post request received")
            print("trying to print json data from request \n", request.get_json())
            print("post request received")
            print("print type of return", type(request.get_json()))
            data_dict = request.get_json()
            user_id = int(data_dict['user_id'])
            end_time = data_dict['end_time']
            session_id = int(data_dict['session_id'])
            query = f"UPDATE {DB_NAME}.sessions SET EndTime = '{end_time}' WHERE SessionID = {session_id} AND UserID = {user_id}"
            print(query)
            my_cur = connection.cursor()
            my_cur.execute(query)
            result = my_cur.fetchall()

            my_cur.close()
            connection.close()
            print("connection closed")
            return jsonify(result)

    except DBConnectionError:
        print("db connection failed")



