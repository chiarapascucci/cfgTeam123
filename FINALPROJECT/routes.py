
import json
import random

from FINALPROJECT import app
from FINALPROJECT.data_access_functions import create_user_in_db, validate_user, DBConnectionError, _connect_to_db, \
    create_new_session
from FINALPROJECT.forms import RegistrationForm, LoginForm
from flask import Flask, jsonify, request, render_template, url_for, redirect, flash
from FINALPROJECT.config import DB_NAME
from FINALPROJECT.guess_my_num import play

from flask import jsonify, request, render_template, url_for, redirect, flash, session
from flask_login import login_user, login_required, logout_user

from FINALPROJECT import app
from FINALPROJECT.ayeshamodels import UserNotFoundException, CustomAuthUser, fetch_user_info_with_username_and_passw
from FINALPROJECT.config import DB_NAME
from FINALPROJECT.data_access_functions import DBConnectionError, _connect_to_db, \
    create_new_session, create_user_in_db
# from flask_bcrypt import Bcrypt
from FINALPROJECT.data_access_functions import mycursor
from FINALPROJECT.forms import RegistrationForm, LoginForm

from FINALPROJECT.tic_tac_toe import receive_move
from Tic_Tac_Game.ticboard import Board

###### this file is a bit of a mess lol ########

########### basic routes ############

@app.route('/')
def home():
    return render_template('home.html', title='home')


@app.route('/start-timer')
def starttimer():
    return render_template('select_break_time.html', title='Start the Timer')


@app.route('/browsegames')
def browsegames():
    return render_template('browsegames.html', title='browsegames')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully')
    return redirect(url_for('home'))


@app.route('/special')
@login_required
def special():
    if 'username' in session:
        print("user session object contains username: ", session)
    return render_template('special.html', title='special')


############# user registration ################

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        username = form.user_name.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        outcome = create_user_in_db(username, first_name, last_name, email, password)
        if outcome:
            flash(f'Account created for {form.user_name.data}!', 'Success')
            return redirect(url_for('login'))
        else:
            flash('something went wrong, please try again')
            return render_template('register.html', title='Register', form=form)
    return render_template('register.html', title='Register', form=form)



#################### user login + authentication ########################


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # if current_user.is_authenticated():
    #     return redirect(url_for('home'))
    if form.validate_on_submit():
        try:
            user_info = fetch_user_info_with_username_and_passw(form.password.data, form.user_name.data)
            user = CustomAuthUser(user_info[0][0], user_info[0][1], user_info[0][2], user_info[0][3],
                                  user_info[0][4], user_info[0][5])
            login_user(user, remember=True)
            session['username'] = user.user_name
            flash('You have been logged in', 'success')
            return redirect(url_for('special'))
        except UserNotFoundException:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='login', form=form)


############## TIMER RELATED views ######################

@app.route('/log-session-start', methods=['GET', 'POST'])
def logsessionstart():
    """will need some way of retrieving user ID"""
    try:
        connection = _connect_to_db()
        if request.method == 'POST':
            print("post request received")

            data_dict = request.get_json()
            user_id = data_dict['user_id']
            start_time = data_dict['start_time']
            req_len = str(data_dict['requested_duration'])
            session_created = create_new_session(user_id, start_time, req_len)
            follow_query = f"select * from {DB_NAME}.sessions WHERE UserID = {user_id} ORDER BY SessionID DESC LIMIT 1;"
            print(follow_query)
            other_cur = connection.cursor()
            other_cur.execute(follow_query)
            result = other_cur.fetchall()
            print("printing result of query to get latest entry: ", result)
            result = jsonify(result)

            other_cur.close()
            connection.close()
            print("connection closed")
            return result

    except DBConnectionError:
        print("db connection failed")


@app.route('/log-session-end', methods=['GET', 'POST'])
def logsessionend():
    try:
        connection = _connect_to_db()
        if request.method == 'POST':
            print("post request received")
            print("trying to print json data from request \n", request.get_json())
            print("post request received")
            print("print type of return", type(request.get_json()))
            data_dict = request.get_json()
            user_id = int(data_dict['user_id'])
            end_time = data_dict['end_time']
            session_id = int(data_dict['session_id'])
            query = f"UPDATE {DB_NAME}.sessions SET EndTime = '{end_time}' WHERE SessionID = {session_id} AND UserID = {user_id};"
            print(query)
            my_cur = connection.cursor()
            my_cur.execute(query)
            result = my_cur.fetchall()
            connection.commit()
            check_query = f"SELECT * FROM {DB_NAME}.sessions WHERE SessionID = {session_id};"
            print("printin check query ", check_query)
            my_cur.execute(check_query)
            check_result = my_cur.fetchall()
            print("printing check result: ", check_result)
            my_cur.close()
            connection.close()
            print("connection closed")
            return jsonify(result)

    except DBConnectionError:
        print("db connection failed")



################################# GAMES RELATED VIEWS ##########################################

#################### TIC TAC TOE #######################

@app.route('/tic-tac-toe')
def tic_tac_toe():
    return render_template('tic_tac.html', title="tictactoe")


@app.route('/tic-tac-ajax', methods=['GET', 'POST'])
def process_tic_tac():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        # state = {}
        x_list = [int(c) for c in data['x']]
        o_list = [int(c) for c in data['o']]
        print(x_list)
        print(o_list)

        board1 = Board(x_list, o_list)

        comp_move = board1.computer_move()
        computer_win = board1.is_a_win("o")
        human_win = board1.is_a_win("x")


################# BLACKJACK ####################


################ TRIVIA #########################


############### GUESS MY NUMBER ##################
