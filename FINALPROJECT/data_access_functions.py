from typing import List

import mysql.connector

from FINALPROJECT.config import DB_NAME, HOST, USER, PASSWORD

db = mysql.connector.connect(host=HOST,
                             user=USER,
                             password=PASSWORD,
                             database=DB_NAME)

mycursor = db.cursor()


class DBConnectionError(Exception):
    pass


def _connect_to_db():
    cnx = mysql.connector.connect(host=HOST,
                                  user=USER,
                                  password=PASSWORD,
                                  auth_plugin='mysql_native_password',
                                  database=DB_NAME)
    return cnx


def get_all_records() -> List:
    db_connection = None
    try:

        db_connection = _connect_to_db()
        cursor = db_connection.cursor()
        query = ""
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



def create_user_in_db(user_name, first_name, last_name, password):
    mycursor.execute("""
    CALL register_user('{}', '{}', '{}', '{}')""".format(user_name, first_name, last_name, password))
    db.commit()
    return True


def validate_user(user_name, password):
    mycursor.execute("""
    CALL validate_user('{}','{}')
    """.format(user_name, password))
    user_id = mycursor.fetchall()
    return user_id


def get_user_first_last_name(user_id):
    mycursor.execute("""
    SELECT FirstName, LastName
    WHERE UserID = {}""".format(user_id))
    user_name = mycursor.fetchall()
    return user_name


def update_last_login_time(user_id):
    mycursor.execute("""
    UPDATE user_info SET
    LastLogin = now()
    WHERE UserID = {};
    """.format(user_id))
    db.commit()
    return True


def create_new_session(user_id, start_time, requested_duration):
    mycursor.execute("""
        INSERT INTO sessions(UserID, StartTime, RequestedDuration)
        VALUES ({}, '{}', {})""".format(user_id, start_time, requested_duration))
    db.commit()
    return True


def create_new_game_record(user_id, game_id, session_id, start_time, end_time):
    mycursor.execute("""
        INSERT INTO game_record(UserID, GameID, SessionID, StartTime, EndTime)
        VALUES ({}, {}, {}, {}, {})""".format(user_id, game_id, session_id, start_time, end_time))
    db.commit()
    return True


def delete_user_from_db(user_id):
    mycursor.execute("""
    DELETE FROM user_info
    WHERE UserID = {}
    """.format(user_id))


def display_total_game_history(user_id):
    mycursor.execute("""
    SELECT g.GameName, r.RecordID, r.StartTime, r.EndTime, s.SessionID, s.StartTime, s.EndTime, s.RequestedDuration
    FROM sessions s
    INNER JOIN
    game_record r
    ON 
    s.SessionID = r.SessionID 
    INNER JOIN 
    game_table g
    ON
    g.GameID = r.GameID
    WHERE s.UserID = {}""".format(user_id))
    user_game_history = mycursor.fetchall()
    return user_game_history

def test_db_connection():
    try:
        cnx = _connect_to_db()
        cur = cnx.cursor()
        query = "show TABLES"
        cur.execute(query)
        result = cur.fetchall()
        print(result)
        cur.close()
        cnx.close()
    except Exception:
        raise DBConnectionError
