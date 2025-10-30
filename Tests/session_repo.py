import unittest
from unittest.mock import MagicMock
from session_repository import SessionRepository

class TestSessionRepository(unittest.TestCase):
    def test_delete_session_success(self):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.rowcount = 1

        repo = SessionRepository(mock_conn)
        result = repo.delete_session(1)

        mock_cursor.execute.assert_called_once_with("DELETE FROM Sessions WHERE session_id = %s", (1,))
        self.assertTrue(result)
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