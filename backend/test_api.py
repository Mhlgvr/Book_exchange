import unittest
import json
from flask import Flask
from __init__ import app
import db

class BooksApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        # Создаем контекст приложения для работы с БД
        self.app_context = app.app_context()
        self.app_context.push()
        self.conn = db.get_db()
        # Очищаем тестовые данные
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM events;")
            cur.execute("DELETE FROM books;")
            self.conn.commit()

    def tearDown(self):
        # Очищаем тестовые данные
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM events;")
            cur.execute("DELETE FROM books;")
            self.conn.commit()
        # Убираем контекст приложения
        self.app_context.pop()

    def test_add_and_get_book(self):
        # Добавление книги
        book_data = {
            "title": "Тестовая книга",
            "author": "Тест Автор",
            "year": 2024,
            "description": "Описание тестовой книги",
            "photo_url": None,
            "point_id": 1,
            "user_id": "testuser"
        }
        response = self.app.post('/api/books', json=book_data)
        self.assertEqual(response.status_code, 201)
        book_id = response.get_json()['id']
        # Получение списка книг
        response = self.app.get('/api/books')
        self.assertEqual(response.status_code, 200)
        books = response.get_json()
        # books[0] = [id, title, author, year, description, photo_url, point_id, user_id]
        self.assertTrue(any(b[0] == book_id for b in books))

    def test_get_books_with_filters(self):
        # Добавляем две книги
        self.app.post('/api/books', json={
            "title": "Книга1",
            "author": "Автор1",
            "year": 2020,
            "description": "desc1",
            "photo_url": None,
            "point_id": 1,
            "user_id": "user1"
        })
        self.app.post('/api/books', json={
            "title": "Книга2",
            "author": "Автор2",
            "year": 2021,
            "description": "desc2",
            "photo_url": None,
            "point_id": 2,
            "user_id": "user2"
        })
        # Фильтр по автору
        response = self.app.get('/api/books?author=Автор1')
        self.assertEqual(response.status_code, 200)
        books = response.get_json()
        self.assertTrue(all('Автор1' in b[2] for b in books))  # author находится в индексе 2
        # Фильтр по точке
        response = self.app.get('/api/books?point_id=2')
        books = response.get_json()
        self.assertTrue(all(b[6] == 2 for b in books))  # point_id находится в индексе 6

    def test_admin_events(self):
        # Добавляем книгу
        self.app.post('/api/books', json={
            "title": "Книга для журнала",
            "author": "Админ",
            "year": 2022,
            "description": "desc",
            "photo_url": None,
            "point_id": 1,
            "user_id": "admin"
        })
        # Получаем журнал событий
        response = self.app.get('/api/admin/events')
        self.assertEqual(response.status_code, 200)
        events = response.get_json()
        # events[0] = [id, book_id, title, event_type, event_time]
        self.assertTrue(any(e[3] == 'added' for e in events))  # event_type находится в индексе 3

if __name__ == '__main__':
    unittest.main() 