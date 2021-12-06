from flask_login import UserMixin

from FINALPROJECT import login_manager
from FINALPROJECT.data_access_functions import mycursor, db


@login_manager.user_loader
def user_loader(user_name):
    user_id = User.get_id(user_name)
    return User.get(user_id)


class UserNotFoundException(Exception):
    pass


class User(UserMixin):

    def __init__(self, user_name, first_name, last_name, email, password):
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.authenticated = False


    def create_user_in_db(self):
        mycursor.execute("""
        INSERT INTO user_info (UserName, FirstName, LastName, PasswordHash)
        VALUES ('{}', '{}', '{}', '{}')""".format(self.user_name, self.first_name, self.last_name, self.password))
        db.commit()
        return True

    def validate_user(self):
        mycursor.execute("""
        SELECT UserID
        FROM user_info
        WHERE PasswordHash = '{}'
        and UserName = '{}'
        """.format(self.password, self.user_name))
        user_id = mycursor.fetchone()[0]
        if user_id is None:
            raise UserNotFoundException()
        return user_id

    def is_active(self):
        return True

    def is_authenticated(self):
        self.authenticated = True
        return self.authenticated

    def get_id(self):
        mycursor.execute("""
        SELECT UserID
        FROM user_info
        WHERE UserName = '{}'
        """.format(self.user_name))
        user_id = mycursor.fetchone()[0]
        return str(user_id).encode('utf-8').decode('utf-8')

    def is_anonymous(self):
        return False
