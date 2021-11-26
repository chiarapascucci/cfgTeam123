import mysql.connector

db = mysql.connector.connect(host='localhost',
                             user="root",
                             password='',
                             database='ayesha_prac')

mycursor = db.cursor()


"""To insert a new user into the DB, I've called the register_user stored procedure.
This will salt a user password with a timestamp and concatenate with the raw password.It then uses the sha2() hash 
algorithm to generate a hashed password. It then inserts username, first & last name, salt and hashed password
 into the columns in table user_id."""


def create_user_in_db(user_name, first_name, last_name, password):
    mycursor.execute("""
    CALL register_user('{}', '{}', '{}', '{}')""".format(user_name, first_name, last_name, password))
    db.commit()
    return True


"""To validate a user's password, I've called the validate_user stored procedure which checks that the username and 
password arguments are the same as the user_name and hashed password stored in the DB. If it is found, it will return 
the UserID and if not it will return nothing."""


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


"""This can be changed depending on the chosen logic - for example, instead of accepting the start and end time 
when creating the session, it can create a new session with just the start time and requested duration, then update
the session with the end time"""


def create_new_session(user_id, start_time, end_time, requested_duration):
    mycursor.execute("""
        INSERT INTO sessions(UserID, StartTime, EndTime, RequestedDuration)
        VALUES ({}, {}, {}, {})""".format(user_id, start_time, end_time, requested_duration))
    db.commit()
    return True


"""This can be changed depending on the chosen logic - for example, instead of accepting the start and end time when 
creating the record, it can create a new record with just the start time, then update the record with the end time"""


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


"""This function will display information relating to user time spent playing a game and the name of that game,
 total session time (time logged in) and any time requested to play. My rationale for including all in the history
 was so that users can see the break down of games played as well as total time spent on app. Not sure if we're timing 
 total time logged in so so this can be changed, and can make this select more detailed or simpler!"""


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
