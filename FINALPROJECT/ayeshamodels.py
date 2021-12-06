from flask_login import UserMixin, AnonymousUserMixin

from FINALPROJECT import login_manager
from FINALPROJECT.data_access_functions import mycursor, db


def fetch_user_info_with_user_id(user_id):
    mycursor.execute("""
    SELECT *
    FROM user_info
    WHERE UserId = {};
    """.format(user_id))
    user_info = mycursor.fetchall()
    return user_info


def fetch_user_info_with_username_and_passw(password, user_name):
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


def get_user_instance(user_info=None, user_id=None):
    if user_info is None and user_id is None:
        return None
    else:
        if user_id is not None and user_info is None:
            user_info = fetch_user_info_with_user_id(user_id)
        user = CustomAuthUser(user_info[0][0], user_info[0][1], user_info[0][2], user_info[0][3], user_info[0][4], user_info[0][5])
        return user



@login_manager.user_loader
def load_user(user_id):
    return get_user_instance(user_id=user_id)


class UserNotFoundException(Exception):
    pass


class CustomAuthUser(UserMixin):
    def __init__(self, user_id, user_name, first_name, last_name, email, password):
        self.user_name = user_name
        self.id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password





