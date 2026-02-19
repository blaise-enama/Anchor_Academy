import unittest
from unittest.mock import MagicMock
from repositories.sessionRepo import SessionRepository

class TestSessionRepository(unittest.TestCase):

    def test_add_session(self):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.rowcount=0
        

    def test_delete_sessions_by_player_success(self):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.rowcount = 3    # pretend that three sessions were deleted

        repo = SessionRepository(mock_conn)
        result = repo.delete_session(1)

        mock_cursor.execure.assert_called_once_with("")

        mock_cursor.execute.assert_called_once_with("DELETE FROM Sessions WHERE session_id = %s", (1,))
        self.assertEqual(result, 3)
        mock_conn.commit.assert_called_once()
        

    def test_delete_session_not_found(self):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.rowcount = 0

        repo = SessionRepository(mock_conn)
        result = repo.delete_session(999)

        self.assertFalse(result)
        mock_conn.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()