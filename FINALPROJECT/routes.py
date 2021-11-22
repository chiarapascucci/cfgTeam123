from typing import List
from flask import Flask, jsonify, request, render_template, url_for
from config import USER, PASSWORD, HOST
import mysql.connector


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

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html', title='home')

@app.route('/tester')
def tester():
    return render_template('tester.html', title='tester')

@app.route('/register')
def register():
    return render_template('register.html', title='Register')


@app.route('/login')
def login():
    return render_template('login.html', title='login')


@app.route('/browsegames')
def browsegames():
    return render_template('browsegames.html', title='browsegames')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
