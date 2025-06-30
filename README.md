# Сервис обмена книгами

Учебный проект сервиса по обмену книгами с REST API и SPA интерфейсом.

## Архитектура

- **Backend**: Flask + PostgreSQL + psycopg
- **Frontend**: React SPA
- **Инфраструктура**: Docker Compose
- **Документация**: Swagger/OpenAPI
- **Тестирование**: unittest

## Быстрый старт

### 1. Клонирование и настройка
```bash
git clone <repository-url>
cd last_night
cp env.example .env
```

### 2. Запуск через Docker Compose
```bash
docker compose up --build
```

### 3. Доступ к сервисам
- **Backend API**: http://localhost:5001
- **Swagger документация**: http://localhost:5001/apidocs/
- **Frontend**: http://localhost:3000

## Структура проекта

```
├── backend/           # Flask API
│   ├── app.py        # Точка входа
│   ├── __init__.py   # Инициализация Flask
│   ├── routes.py     # API endpoints
│   ├── db.py         # Работа с БД
│   ├── models.sql    # Схема БД
│   └── test_api.py   # Тесты
├── frontend/         # React SPA
├── docker-compose.yml
└── .env              # Переменные окружения
```

## API Endpoints

### Книги
- `GET /api/books` - список книг с фильтрами
- `POST /api/books` - добавление книги
- `GET /api/books/user/<user_id>` - книги пользователя

### Точки обмена
- `GET /api/points` - список точек обмена

### Админ
- `GET /api/admin/books` - все книги
- `GET /api/admin/events` - журнал событий

## Переменные окружения

Создайте файл `.env` в корне проекта:

```env
# Database
DB_NAME=books_exchange
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# Flask
FLASK_ENV=development
FLASK_DEBUG=True
```

## Тестирование

### Backend тесты
```bash
docker compose exec backend python -m unittest test_api.py -v
```

### Frontend тесты
```bash
cd frontend
npm test
```

## Разработка

### Локальный запуск backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Локальный запуск frontend
```bash
cd frontend
npm install
npm start
```

## Функциональность

### Пользователи могут:
- Просматривать доступные книги
- Искать и фильтровать книги
- Добавлять свои книги для обмена
- Просматривать свои книги

### Администраторы могут:
- Просматривать все книги
- Видеть журнал событий (добавление/удаление книг)

## Технологии

- **Backend**: Python, Flask, PostgreSQL, psycopg, flasgger
- **Frontend**: React, nginx
- **DevOps**: Docker, Docker Compose
- **Тестирование**: unittest, React Testing Library 