from flask_login import UserMixin, login_manager, LoginManager
from FINALPROJECT import login_manager
from FINALPROJECT.data_access_functions import mycursor, db


@login_manager.user_loader
def user_loader(user_name):
    mycursor.execute("""
        SELECT UserID
        FROM user_info
        WHERE UserName = '{}'
        """.format(user_name))
    user_id = mycursor.fetchone()[0]
    if user_id is None:
        raise UserNotFoundException()
    return user_id


class UserNotFoundException(Exception):
    pass


class User:

    def __init__(self, user_name, first_name, last_name, email, password):
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

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
        return self.authenticated

    def get_id(self):
        """ This method must return a unicode that uniquely identifies this user, and can be used to load the user
        from the user_loader callback. Note that this must be a unicode - if the ID is natively an int or some other
        type, you will need to convert it to unicode. """
        pass

    def is_anonymous(self):
        return False
