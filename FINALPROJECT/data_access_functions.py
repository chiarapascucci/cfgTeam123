import mysql.connector
from FINALPROJECT.config import DB_NAME, HOST, USER, PASSWORD
import FINALPROJECT

global db, mycursor


# decorator for all functions that hit database
def connect_to_db(func):
    def inner_func(*args, **kwargs):
        global db, mycursor
        db = mysql.connector.connect(host=HOST,
                                     user=USER,
                                     password=PASSWORD,
                                     # for unit testing the reference has to be fully qualified
                                     database=FINALPROJECT.config.DB_NAME)
        mycursor = db.cursor(buffered=True)
        result = func(*args, **kwargs)
        mycursor.close()
        db.close()
        return result
    return inner_func


@connect_to_db
def create_user_in_db(user_name, first_name, last_name, password, email=None):
    mycursor.execute("""
    INSERT INTO user_info (UserName, FirstName, LastName, PasswordHash, Email) 
    VALUES ('{}', '{}', '{}', '{}', '{}')""".format(user_name, first_name, last_name, password, email))
    db.commit()
    query = "SELECT UserID FROM user_info WHERE UserName = '{}' ".format(user_name)
    mycursor.execute(query)
    result = mycursor.fetchall()
    return True


@connect_to_db
def validate_user(user_name, hashed_password):
    mycursor.execute("""
    SELECT UserID
    FROM user_info
    WHERE PasswordHash = '{}'
    and UserName = '{}'
    """.format(hashed_password, user_name))
    user_id = mycursor.fetchone()[0]
    if user_id is None:
        raise UserNotFoundException()
    return user_id


class UserNotFoundException(Exception):
    pass

@connect_to_db
def create_new_session(user_id, start_time, requested_duration):
    mycursor.execute("""
        INSERT INTO sessions(UserID, StartTime, RequestedDuration)
        VALUES ({}, '{}', {})""".format(user_id, start_time, requested_duration))
    db.commit()
    return mycursor.lastrowid


@connect_to_db
def get_session_id(user_id):
    mycursor.execute("""
        SELECT SessionID 
        FROM sessions
        WHERE UserID = {}
        ORDER BY SessionID DESC
        """.format(user_id))
    # fetchone() returns a tuple e.g. (5, ), [0] accesses first element in tuple - which is user_id
    session_id = mycursor.fetchone()[0]
    if session_id is None:
        raise UserNotFoundException()
    return session_id


@connect_to_db
def update_session_end_time(end_time, session_id, user_id):
    mycursor.execute(f"UPDATE {DB_NAME}.sessions SET EndTime = '{end_time}' WHERE SessionID = {session_id} A"
                     f"ND UserID = {user_id};")
    db.commit()



@connect_to_db
def create_new_game_record(user_id, game_id, session_id):
    mycursor.execute("""
        INSERT INTO game_record(UserID, GameID, SessionID, StartTime)
        VALUES ({}, {}, {}, now())""".format(user_id, game_id, session_id))
    db.commit()
    return mycursor.lastrowid


@connect_to_db
def log_game_record_end_time(record_id):
    mycursor.execute("""
        UPDATE game_record
        SET EndTime = now()
        WHERE RecordID = {}
        """.format(record_id))
    db.commit()
    return mycursor.lastrowid


@connect_to_db
def delete_user_from_db(user_id):
    mycursor.execute("""
    DELETE FROM user_info
    WHERE UserID = {}
    """.format(user_id))


@connect_to_db
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


# function used when instantiating a user object

def fetch_user_info_with_user_id(user_id):
    db = mysql.connector.connect(host=HOST,
                                 user=USER,
                                 password=PASSWORD,
                                 # for unit testing the reference has to be fully qualified
                                 database=FINALPROJECT.config.DB_NAME)
    mycursor = db.cursor()
    mycursor.execute("""
    SELECT *
    FROM user_info
    WHERE UserId = {};
    """.format(user_id))
    user_info = mycursor.fetchall()
    return user_info


# function used when instantiating a user object

def fetch_user_info_with_username(user_name):
    db = mysql.connector.connect(host=HOST,
                                 user=USER,
                                 password=PASSWORD,
                                 # for unit testing the reference has to be fully qualified
                                 database=FINALPROJECT.config.DB_NAME)
    mycursor = db.cursor()
    mycursor.execute("""
    SELECT *
    FROM user_info
    WHERE UserName = '{}'
    """.format(user_name))
    user_info = mycursor.fetchall()
    if user_info is None:
        raise UserNotFoundException()
    return user_info
