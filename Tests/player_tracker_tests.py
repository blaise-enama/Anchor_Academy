import unittest
import mysql.connector
import pymysql
from unittest.mock import patch, MagicMock
from player_tracker import connect_to_database


class TestDatabaseConncection(unittest.TestCase):

    @patch("pymysql.connect")
    def test_connection_success(self, mock_connect):
        # Arrange: mock successful connection
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        # Act
        conn = connect_to_database('localhost','root', 'Enamfam.7', 'Anchor_Academy',driver='pymysql')

        # Assert
        mock_connect.assert_called_once_with(
            host="localhost",
            user="root",
            passwd="fakepassword",
            db="Anchor_Academy", # substitute with test_academy
            driver="pymysql"
        )

        self.assertEqual(conn, mock_conn)


    @patch("pymysql.connect", side_effect=Exception("Connection failed"))
    def test_connection_failure(self,mock_connect):
        #simulate mysql throwing an error
        mock_connect.side_effect = mysql.connection.Error("Unable to establisn a connection")
        
        #simulate pymysql throwing an error
        mock_connect.side_effect = pymysql.err.OperationalError(203, "Can't connect to the MySQL server")


        # Act
        conn = connect_to_database(
            "localhost", 
            "root@localhost", 
            "notthepassword", 
            "test_db",
            driver="pymysql")

        # Assert
        mock_connect.assert_called_once()
        self.assertIsNone(conn)


if __name__ == "__main__":
    unittest.main()
