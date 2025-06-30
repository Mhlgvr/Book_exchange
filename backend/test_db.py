import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import db

class TestDatabase(unittest.TestCase):
    def setUp(self):
        """Настройка перед каждым тестом"""
        pass

    def tearDown(self):
        """Очистка после каждого теста"""
        pass

    @patch('db.get_db')
    def test_get_exchange_points(self, mock_get_db):
        """Тест получения точек обмена"""
        # Подготавливаем мок
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            {'id': 1, 'address': 'Точка 1'},
            {'id': 2, 'address': 'Точка 2'}
        ]
        mock_get_db.return_value = mock_conn

        # Выполняем тест
        result = db.get_exchange_points()

        # Проверяем результат
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['id'], 1)
        self.assertEqual(result[0]['address'], 'Точка 1')
        self.assertEqual(result[1]['id'], 2)
        self.assertEqual(result[1]['address'], 'Точка 2')

    @patch('db.get_db')
    def test_add_book(self, mock_get_db):
        """Тест добавления книги"""
        # Подготавливаем мок
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {'id': 1}
        mock_get_db.return_value = mock_conn

        # Выполняем тест
        result = db.add_book(
            'Тестовая книга',
            'Тестовый автор',
            2024,
            'Описание',
            'http://example.com/cover.jpg',
            1,
            None,
            'user_1'
        )

        # Проверяем результат
        self.assertEqual(result, 1)
        mock_cursor.execute.assert_called_once()

    @patch('db.get_db')
    def test_get_books_with_filters(self, mock_get_db):
        """Тест получения книг с фильтрами"""
        # Подготавливаем мок
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            {
                'id': 1,
                'title': 'Тестовая книга',
                'author': 'Тестовый автор',
                'year': 2024,
                'user_id': None
            }
        ]
        mock_get_db.return_value = mock_conn

        # Выполняем тест
        filters = {'author': 'Тестовый', 'year': 2024}
        result = db.get_books(filters)

        # Проверяем результат
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['title'], 'Тестовая книга')
        self.assertEqual(result[0]['author'], 'Тестовый автор')

    @patch('db.get_db')
    def test_get_book(self, mock_get_db):
        """Тест получения одной книги"""
        # Подготавливаем мок
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {
            'id': 1,
            'title': 'Тестовая книга',
            'author': 'Тестовый автор'
        }
        mock_get_db.return_value = mock_conn

        # Выполняем тест
        result = db.get_book(1)

        # Проверяем результат
        self.assertEqual(result['id'], 1)
        self.assertEqual(result['title'], 'Тестовая книга')

    @patch('db.get_db')
    def test_take_book(self, mock_get_db):
        """Тест взятия книги"""
        # Подготавливаем мок
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_db.return_value = mock_conn

        # Выполняем тест
        db.take_book(1, 'user_1')

        # Проверяем, что execute был вызван
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()

    @patch('db.get_db')
    def test_get_user_books(self, mock_get_db):
        """Тест получения книг пользователя"""
        # Подготавливаем мок
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            {
                'id': 1,
                'title': 'Моя книга',
                'added_by': 'user_1'
            }
        ]
        mock_get_db.return_value = mock_conn

        # Выполняем тест
        result = db.get_user_books('user_1')

        # Проверяем результат
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['title'], 'Моя книга')
        self.assertEqual(result[0]['added_by'], 'user_1')

    @patch('db.get_db')
    def test_log_event(self, mock_get_db):
        """Тест логирования события"""
        # Подготавливаем мок
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_get_db.return_value = mock_conn

        # Выполняем тест
        db.log_event(1, 'test_event')

        # Проверяем, что execute был вызван
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()

    @patch('db.get_db')
    def test_get_events(self, mock_get_db):
        """Тест получения событий"""
        # Подготавливаем мок
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            {
                'id': 1,
                'book_id': 1,
                'title': 'Тестовая книга',
                'event_type': 'added',
                'event_time': '2024-01-01 12:00:00'
            }
        ]
        mock_get_db.return_value = mock_conn

        # Выполняем тест
        result = db.get_events()

        # Проверяем результат
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['event_type'], 'added')
        self.assertEqual(result[0]['title'], 'Тестовая книга')

if __name__ == '__main__':
    unittest.main() 