from typing import List
from flask import Flask, jsonify, request, render_template, url_for
from config import USER, PASSWORD, HOST
import mysql.connector
import json


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
        connection = _connect_to_db("test")
        if request.method == 'POST':
            print("post request received")
            print("trying to print json data from request \n", request.get_json())
            print("post request received")
            print("print type of return", type(request.get_json()))
            data_dict = request.get_json()
            user_id = data_dict['user_id']
            start_time = data_dict['start_time']
            req_len = str(data_dict['requested_duration'])
            query = f"INSERT INTO test.sessions (UserID, StartTimer, RequestedDuration) VALUES ('{user_id}', '{start_time}', '{req_len}');"
            print(query)
            my_cur = connection.cursor()
            my_cur.execute(query)
            result = my_cur.fetchall()
            print(result)
            my_cur.close()
            connection.close()
            print("connection closed")

    except DBConnectionError:
        print("db connection failed")


@app.route('/log-session-end', methods=['GET', 'POST'])
def logsessionend():
    pass


if __name__ == '__main__':
    app.run(debug=True, port=5000)
