from FINALPROJECT import app
from FINALPROJECT.data_access_functions import test_db_connection

if __name__ == '__main__':
    test_db_connection()
    app.run(debug=True, port=5000)

