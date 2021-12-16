from unittest import TestCase
from unittest.mock import patch

import mysql.connector
from FINALPROJECT.data_access_functions import create_user_in_db, validate_user
from FINALPROJECT.config import HOST, USER, PASSWORD

"""
Unit tests using test_db (created in mysql with schema for productivity_app db for testing purposes)
Tests check:
a connection is made with the test database
a new user is created in the test database, returns user_id
a user can be validated using their username and password, returns user_id
a user name can be fetched with a user_id
"""


class TestDataFunctions(TestCase):
    # creates tables and inserts user for each test
    def setUp(self):
        self.db = mysql.connector.connect(host=HOST,
                                          user=USER,
                                          password=PASSWORD,
                                          database="test_db")
        self.mycursor = self.db.cursor()
        self.mycursor.execute("DELETE FROM user_info WHERE UserID > 0")
        self.mycursor.execute("""
            INSERT INTO user_info (UserID, UserName, FirstName, LastName, PasswordHash, Email) 
            VALUES (1, '{}', '{}', '{}', '{}', '{}')""".format("sample_username", "sample_first_name",
                                                               "sample_last_name",
                                                               "sample_password", "sample_email"))
        self.db.commit()

    # clears tables
    def tearDown(self):
        self.mycursor.execute("DELETE FROM user_info WHERE UserID > 0")
        self.db.commit()

    @patch("FINALPROJECT.config.DB_NAME", "test_db")
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

    # validates a sample user (with a user_id of 1)
    @patch("FINALPROJECT.config.DB_NAME", "test_db")
    def test_validate_user(self):
        user_id = validate_user("sample_username", "sample_password")
        self.assertEqual(user_id, 1)
