from unittest.mock import MagicMock
from unittest import TestCase, main, mock
from FINALPROJECT.data_access_functions import initialise_db

import mysql.connector

from FINALPROJECT.data_access_functions import create_user_in_db, validate_user, get_user_first_last_name, \
    update_last_login_time, create_new_session, create_new_game_record, delete_user_from_db, display_total_game_history


class TestDataFunctions(TestCase):

    def test_create_user_in_db(self):
        dbc = MagicMock()
        cursor = MagicMock()
        initialise_db(dbc, cursor)
        test_data = create_user_in_db("TestUserName", "TestFirstName", "TestLastName", "TestPasswordHash", "TestEmail")
        call_args = cursor.execute.call_args
        self.assertTrue(cursor.execute.called)
        self.assertIn("TestUserName", str(call_args.args))

    def test_validate_user(self):
        pass

    def test_get_user_name(self):
        pass

    def test_update_login(self):
        pass

    def test_new_session(self):
        pass

    def test_new_game(self):
        pass

    def test_delete_user(self):
        pass

    def test_display_history(self):
        pass
