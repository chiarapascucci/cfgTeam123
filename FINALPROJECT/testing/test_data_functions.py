from unittest import TestCase, main, mock
import mysql.connector
from FINALPROJECT.data_access_functions import create_user_in_db, validate_user, get_user_first_last_name, initialise_db, \
    update_last_login_time, create_new_session, create_new_game_record, delete_user_from_db, display_total_game_history
from FINALPROJECT.config import HOST, USER, PASSWORD


class TestDataFunctions(TestCase):

    def setUp(self):
        self.db = mysql.connector.connect(host=HOST,
                                     user=USER,
                                     password=PASSWORD,
                                     database="test_db")
        self.mycursor = self.db.cursor()
        initialise_db(self.db, self.mycursor)
        self.mycursor.execute("DELETE FROM user_info WHERE UserID > 0")
        self.mycursor.execute("""
            INSERT INTO user_info (UserID, UserName, FirstName, LastName, PasswordHash, Email) 
            VALUES (1, '{}', '{}', '{}', '{}', '{}')""".format("sample_username", "sample_first_name", "sample_last_name",
                                                            "sample_password", "sample_email"))
        self.db.commit()

    def tearDown(self):
        self.mycursor.execute("DELETE FROM user_info WHERE UserID > 0")
        self.db.commit()

    # Using test_db (created in mysql with schema for productivity_app db for testing purposes)

    def test_create_user_in_db_(self):
        test_user_name = "TestUserName"
        test_hashed_password = "TestPasswordHash"
        create_user_in_db(test_user_name, "TestFirstName", "TestLastName", test_hashed_password, "TestEmail")
        self.mycursor.execute("""
        SELECT UserID
        FROM user_info
        WHERE PasswordHash = '{}'
        and UserName = '{}'
        """.format(test_hashed_password, test_user_name))
        test_user_id = self.mycursor.fetchone()[0]
        self.assertIsNotNone(test_user_id)

    def test_validate_user(self):
        user_id = validate_user("sample_username", "sample_password")
        self.assertEqual(user_id, 1)

    def test_get_user_name(self):
        first_name, last_name = get_user_first_last_name(1)
        self.assertEqual("sample_first_name", first_name)
        self.assertEqual("sample_last_name", last_name)


