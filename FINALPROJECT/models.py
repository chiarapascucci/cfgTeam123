from flask_login import UserMixin, AnonymousUserMixin
import mysql.connector

from FINALPROJECT import login_manager, HOST, USER, PASSWORD
from FINALPROJECT.config import DB_NAME
from FINALPROJECT.data_access_functions import mycursor, db, create_user_in_db
from werkzeug.security import generate_password_hash, check_password_hash


def fetch_user_info_with_user_id(user_id):
    db = mysql.connector.connect(host=HOST,
                                 user=USER,
                                 password=PASSWORD,
                                 database=DB_NAME)
    mycursor = db.cursor()
    mycursor.execute("""
    SELECT *
    FROM user_info
    WHERE UserId = {};
    """.format(user_id))
    user_info = mycursor.fetchall()
    return user_info


def fetch_user_info_with_username(user_name):
    db = mysql.connector.connect(host=HOST,
                                 user=USER,
                                 password=PASSWORD,
                                 database=DB_NAME)
    mycursor = db.cursor()
    mycursor.execute("""
    SELECT *
    FROM user_info
    WHERE UserName = '{}'
    """.format(user_name))
    user_info = mycursor.fetchall()
    if user_info is None:
        raise UserNotFoundException()
    print(user_info)
    return user_info


def get_user_instance(user_info=None, user_id=None, user_name=None):
    if user_info is None and user_id is None and user_name is None:
        return None
    else:
        if user_info is None:
            if user_id is not None:
                user_info = fetch_user_info_with_user_id(user_id)
            elif user_name is not None:
                user_info = fetch_user_info_with_username(user_name)
        print(user_info[0][5])
        user = CustomAuthUser(user_name=user_info[0][1], first_name=user_info[0][2], last_name=user_info[0][3],
                              email=user_info[0][4], password=user_info[0][5], user_id=user_info[0][0])
        return user



@login_manager.user_loader
def load_user(user_id):
    return get_user_instance(user_id=user_id)


class UserNotFoundException(Exception):
    pass


class CustomAuthUser(UserMixin):
    def __init__(self, user_name, first_name, last_name, email, password, user_id=None):
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.id = user_id

    def verify_password(self, pwd):
        result = check_password_hash(self.password, pwd)
        print(self.password)
        print(pwd)
        print(generate_password_hash(pwd))
        print(result)
        return result

    def save(self):
        self.password = generate_password_hash(self.password)
        user_id = create_user_in_db(self.user_name, self.first_name, self.last_name, self.password, self.email)
        self.id = user_id
