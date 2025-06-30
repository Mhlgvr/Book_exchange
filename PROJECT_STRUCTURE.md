# Структура проекта

```
last_night/
├── README.md                    # Основная документация проекта
├── PROJECT_STRUCTURE.md         # Этот файл - описание структуры
├── env.example                  # Шаблон переменных окружения
├── .gitignore                   # Исключения для git (общий для всего проекта)
├── docker-compose.yml           # Конфигурация Docker Compose
│
├── backend/                     # Flask API Backend
│   ├── Dockerfile              # Docker образ для backend
│   ├── requirements.txt        # Python зависимости
│   ├── app.py                  # Точка входа Flask приложения
│   ├── __init__.py             # Инициализация Flask приложения
│   ├── routes.py               # API endpoints с Swagger документацией
│   ├── db.py                   # Работа с базой данных (все SQL запросы)
│   ├── models.sql              # Схема базы данных
│   └── test_api.py             # Тесты API (unittest)
│
└── frontend/                    # React SPA Frontend
    ├── Dockerfile              # Docker образ для frontend
    ├── package.json            # Node.js зависимости
    ├── package-lock.json       # Фиксированные версии зависимостей
    ├── public/                 # Статические файлы
    │   ├── index.html          # Главная HTML страница
    │   ├── favicon.ico         # Иконка сайта
    │   ├── manifest.json       # PWA манифест
    │   ├── robots.txt          # Для поисковых роботов
    │   └── logo*.png           # Логотипы
    └── src/                    # Исходный код React
        ├── index.js            # Точка входа React приложения
        ├── index.css           # Глобальные стили
        ├── App.js              # Главный компонент
        ├── App.css             # Стили главного компонента
        ├── App.test.js         # Тесты главного компонента
        ├── logo.svg            # SVG логотип
        ├── reportWebVitals.js  # Метрики производительности
        ├── setupTests.js       # Настройка тестов
        ├── service-worker.js   # Service Worker для PWA
        └── serviceWorkerRegistration.js # Регистрация SW
```

## Принципы организации

### ✅ Правильно расположенные файлы:
- **Конфигурационные файлы** в корне проекта
- **Dockerfile'ы** в своих папках (backend/, frontend/)
- **Зависимости** рядом с кодом (requirements.txt, package.json)
- **Тесты** рядом с тестируемым кодом
- **Схема БД** в backend (models.sql)

### ❌ Что было исправлено:
- Удален дублирующий `.gitignore` из frontend/
- Удален вложенный `.git/` репозиторий из frontend/
- Удален `__pycache__/` из backend/
- Перенесены README, .env, .gitignore в корень

### 📁 Стандартные папки:
- `backend/` - весь код backend
- `frontend/` - весь код frontend  
- `public/` - статические файлы React
- `src/` - исходный код React

### 🔧 Конфигурация:
- Один `.env` файл в корне для всего проекта
- Один `.gitignore` в корне для всего проекта
- `docker-compose.yml` в корне для оркестрации 