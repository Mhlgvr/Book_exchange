import unittest
import json
from unittest.mock import patch, MagicMock
from flask import Flask
from __init__ import app
import db

class BooksApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        # Создаем контекст приложения для работы с БД
        self.app_context = app.app_context()
        self.app_context.push()
        
        # Мокаем функции базы данных
        self.db_patcher = patch('db.get_db')
        self.mock_get_db = self.db_patcher.start()
        
        # Создаем мок соединения
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_conn.cursor.return_value.__enter__.return_value = self.mock_cursor
        self.mock_get_db.return_value = self.mock_conn

    def tearDown(self):
        # Останавливаем моки
        self.db_patcher.stop()
        # Убираем контекст приложения
        self.app_context.pop()

    @patch('db.add_book')
    @patch('db.get_books')
    def test_add_and_get_book(self, mock_get_books, mock_add_book):
        # Настраиваем моки
        mock_add_book.return_value = 1
        mock_get_books.return_value = [
            {
                'id': 1,
                'title': 'Тестовая книга',
                'author': 'Тест Автор',
                'year': 2024,
                'description': 'Описание тестовой книги',
                'photo_url': None,
                'point_id': 1,
                'user_id': None,
                'added_by': 'user_1'
            }
        ]
        
        # Добавление книги
        book_data = {
            "title": "Тестовая книга",
            "author": "Тест Автор",
            "year": 2024,
            "description": "Описание тестовой книги",
            "photo_url": None,
            "point_id": 1
        }
        response = self.app.post('/api/books/add', json=book_data)
        self.assertEqual(response.status_code, 201)
        book_id = response.get_json()['book_id']
        self.assertEqual(book_id, 1)
        
        # Получение списка книг
        response = self.app.get('/api/books')
        self.assertEqual(response.status_code, 200)
        books = response.get_json()
        # Проверяем, что книга добавлена
        self.assertTrue(any(b['title'] == "Тестовая книга" for b in books))

    @patch('db.add_book')
    @patch('db.get_books')
    def test_get_books_with_filters(self, mock_get_books, mock_add_book):
        # Настраиваем моки
        mock_add_book.return_value = 1
        
        # Мокаем разные ответы для разных фильтров
        def get_books_side_effect(filters=None):
            if filters and 'author' in filters and filters['author'] == 'Автор1':
                return [
                    {
                        'id': 1,
                        'title': 'Книга1',
                        'author': 'Автор1',
                        'year': 2020,
                        'point_id': 1
                    }
                ]
            elif filters and 'point_id' in filters and filters['point_id'] == 2:
                return [
                    {
                        'id': 2,
                        'title': 'Книга2',
                        'author': 'Автор2',
                        'year': 2021,
                        'point_id': 2
                    }
                ]
            else:
                return []
        
        mock_get_books.side_effect = get_books_side_effect
        
        # Фильтр по автору
        response = self.app.get('/api/books?author=Автор1')
        self.assertEqual(response.status_code, 200)
        books = response.get_json()
        self.assertTrue(all('Автор1' in b['author'] for b in books))
        
        # Фильтр по точке
        response = self.app.get('/api/books?point_id=2')
        books = response.get_json()
        self.assertTrue(all(b['point_id'] == 2 for b in books))

    @patch('db.add_book')
    @patch('db.get_events')
    def test_admin_events(self, mock_get_events, mock_add_book):
        # Настраиваем моки
        mock_add_book.return_value = 1
        mock_get_events.return_value = [
            {
                'id': 1,
                'book_id': 1,
                'title': 'Книга для журнала',
                'event_type': 'added_by_user',
                'event_time': '2024-01-01 12:00:00'
            }
        ]
        
        # Получаем журнал событий
        response = self.app.get('/api/admin/events')
        self.assertEqual(response.status_code, 200)
        events = response.get_json()
        # Проверяем, что есть событие добавления книги
        self.assertTrue(any(e['event_type'] == 'added_by_user' for e in events))

if __name__ == '__main__':
    unittest.main() 