from FINALPROJECT.data_access_functions import mycursor, db


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
