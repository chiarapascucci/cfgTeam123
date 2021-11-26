from typing import List
from flask import Flask, jsonify, request, render_template, url_for
from config import USER, PASSWORD, HOST
import mysql.connector
import json

DB_NAME = 'timer_test'
class DBConnectionError(Exception):
    pass


def _connect_to_db(db_name: str):
    cnx = mysql.connector.connect(host=HOST,
                                  user=USER,
                                  password=PASSWORD,
                                  auth_plugin='mysql_native_password',
                                  database='timer_test')
    return cnx


def get_all_records() -> List:
    db_connection = None
    try:
        db_name = DB_NAME
        db_connection = _connect_to_db(db_name)
        cursor = db_connection.cursor()
        query = "SELECT * FROM timer_test.user_info"
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


app = Flask(__name__)

"""
https://hackersandslackers.com/configure-flask-applications/
above is link with info about app.config for when you want to encrypt information i think
"""

get_all_records()


@app.route('/')
def home():
    return render_template('home.html', title='home')


@app.route('/register')
def register():
    return render_template('register.html', title='Register')


@app.route('/login')
def login():
    return render_template('login.html', title='login')


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


if __name__ == '__main__':
    app.run(debug=True, port=5000)
