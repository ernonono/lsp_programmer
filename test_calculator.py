import unittest
from unittest.mock import MagicMock

class HistoryManager:
    def __init__(self, db):
        self.db = db
        self.cursor = self.db.cursor()
    
    def fetch_history(self):
        self.cursor.execute("SELECT expression, result FROM history ORDER BY id DESC")
        return self.cursor.fetchall()

    def insert_history(self, expression, result):
        self.cursor.execute("INSERT INTO history (expression, result) VALUES (%s, %s)", (expression, result))
        self.db.commit()

    def delete_all_history(self):
        self.cursor.execute("DELETE FROM history")
        self.db.commit()
        self.histories = []
        self.update_history_expression('')
        self.update_expression('')

    def update_history_expression(self, expression):
        # Dummy implementation for unit test
        pass

    def update_expression(self, expression):
        # Dummy implementation for unit test
        pass

class TestHistoryManager(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_db.cursor.return_value = self.mock_cursor
        self.history_manager = HistoryManager(self.mock_db)

    def test_fetch_history(self):
        expected_result = [("1+1", "2"), ("2+2", "4")]
        self.mock_cursor.fetchall.return_value = expected_result

        result = self.history_manager.fetch_history()

        self.mock_cursor.execute.assert_called_once_with("SELECT expression, result FROM history ORDER BY id DESC")
        self.assertEqual(result, expected_result)

    def test_insert_history(self):
        expression = "3+3"
        result = "6"

        self.history_manager.insert_history(expression, result)

        self.mock_cursor.execute.assert_called_once_with("INSERT INTO history (expression, result) VALUES (%s, %s)", (expression, result))
        self.mock_db.commit.assert_called_once()

    def test_delete_all_history(self):
        self.history_manager.delete_all_history()

        self.mock_cursor.execute.assert_called_once_with("DELETE FROM history")
        self.mock_db.commit.assert_called_once()
        self.assertEqual(self.history_manager.histories, [])

if __name__ == '__main__':
    unittest.main()
