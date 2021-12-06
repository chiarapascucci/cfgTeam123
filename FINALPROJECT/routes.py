# import json
# bcrypt = Bcrypt(app)
# import bcrypt
from FINALPROJECT.ayeshamodels import User, UserNotFoundException
from FINALPROJECT import app
from FINALPROJECT.data_access_functions import create_user_in_db, validate_user, DBConnectionError, _connect_to_db, \
    create_new_session
from FINALPROJECT.forms import RegistrationForm, LoginForm
from flask import Flask, jsonify, request, render_template, url_for, redirect, flash

from FINALPROJECT.config import DB_NAME
from FINALPROJECT.tic_tac_toe import receive_move
from flask_login import login_user, login_required, logout_user, utils, current_user

# from flask_bcrypt import Bcrypt
from FINALPROJECT.data_access_functions import mycursor


@app.route('/')
def home():
    return render_template('home.html', title='home')


def fetch_user_info(password, user_name):
    mycursor.execute("""
    SELECT *
    FROM user_info
    WHERE PasswordHash = '{}'
    and UserName = '{}'
    """.format(password, user_name))
    user_info = mycursor.fetchall()
    if user_info is None:
        raise UserNotFoundException()
    return user_info


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(form.user_name.data, form.first_name.data, form.last_name.data, form.email.data, form.password.data)
        user.create_user_in_db()
        flash(f'Account created for {form.user_name.data}!', 'Success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        try:
            user_info = fetch_user_info(form.password.data, form.user_name.data)
            user = User(user_info[0][1], user_info[0][2], user_info[0][3], user_info[0][4], user_info[0][5])
            user.authenticated = True
            login_user(user, remember=True)
            flash('You have been logged in', 'success')
            return redirect(url_for('special'))
        except UserNotFoundException:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='login', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully')
    return redirect(url_for('home'))


@app.route('/special')
@login_required
def special():
    return 'You are logged in'


# @app.route('/dashboard')
# @login_required
# def dashboard():
#     return render_template('dashboard.html', title='dashboard')


@app.route('/tic-tac-toe')
def tic_tac():
    return render_template('tic_tac.html', title='Tic Tac Toe!')


@app.route('/tic-tac-toe-ajax')
def process_tic_tac_toe():
    pass


@app.route('/start-timer')
def starttimer():
    return render_template('select_break_time.html', title='Start the Timer')


@app.route('/browsegames')
def browsegames():
    return render_template('browsegames.html', title='browsegames')


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


@app.route('/play-tic-tac-toe')
def tic_tac_toe():
    return render_template('tic_tac.html', title="tictactoe")


@app.route('/tic-tac-ajax', methods=['GET', 'POST'])
def process_tic_tac():
    if request.method == 'POST':
        data = request.get_json()

        print(data)
        state = {}
        x_list = [int(c) for c in data['x']]
        o_list = [int(c) for c in data['o']]
        print(x_list)
        print(o_list)

        state['x'] = set(x_list)
        state['o'] = set(o_list)

        result = receive_move(state)
        return jsonify(result)
