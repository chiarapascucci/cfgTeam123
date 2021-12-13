from flask_login import UserMixin
from FINALPROJECT import login_manager
from FINALPROJECT.data_access_functions import create_user_in_db, fetch_user_info_with_user_id, \
    fetch_user_info_with_username
from werkzeug.security import generate_password_hash, check_password_hash


# helper function to load_user
def get_user_instance(user_info=None, user_id=None, user_name=None):
    """
    :param user_info:
    :param user_id:
    :param user_name:
    :return: instance of user object

    helper function to load user
    this function returns an instance of a user object
    it can take the full [tuple] of user info
    or given a unique ID or username it can fetch those information from the DB
    so to be able to create an instance of user
    """
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


# user loader needed by flask login
# it simple takes a unique identifier (user id), which correspond to a user entry in the DB
# using this ID it returns an instance of a user obj
@login_manager.user_loader
def load_user(user_id):
    return get_user_instance(user_id=user_id)


class UserNotFoundException(Exception):
    pass

# python class to represent users and hold user data
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
        return result

    # this method is called when the user is first created in the DB
    def save(self):
        self.password = generate_password_hash(self.password)
        user_id = create_user_in_db(self.user_name, self.first_name, self.last_name, self.password, self.email)
        self.id = user_id
