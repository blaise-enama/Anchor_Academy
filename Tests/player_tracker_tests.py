import unittest
import mysql.connector
from unittest.mock import patch, MagicMock
from player_tracker import connect_to_database


class TestDatabaseConncection(unittest.TestCase):

    @patch("player_tracker.mysql.connector.connect")
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
            db="Anchor_Academy" # substitute with test_academy
        )

        self.assertEqual(conn, mock_conn)


    @patch("player_tracker.mysql.connector.connect", side_effect=Exception("Connection failed"))
    def test_connection_failure(self,mock_connect):
        #simulate mysql throwing an error
        mock_connect.side_effect = mysql.connector.Error("Unable to establisn a connection")

        # Act
        conn = connect_to_database(
            "localhost", 
            "root@localhost", 
            "notthepassword", 
            "test_db")

        # Assert
        mock_connect.assert_called_once()
        self.assertIsNone(conn)


if __name__ == "__main__":
    unittest.main()
