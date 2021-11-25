import mysql.connector

db = mysql.connector.connect(host="34.89.124.173",
                             user="root",
                             password="cfgteam123",
                             database="productivity_app")

mycursor = db.cursor()


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
