# CI/CD Pipeline для Сервиса Обмена Книгами

## 🚀 Обзор

Проект настроен с полноценным CI/CD pipeline на GitHub Actions, который автоматически тестирует, собирает и деплоит приложение.

## 📋 Структура Pipeline

### 1. Тестирование (Test Job)
- **Backend тесты**: unittest для API и функций базы данных
- **Frontend тесты**: Jest + React Testing Library
- **Интеграционные тесты**: тестирование с реальной базой данных
- **Покрытие кода**: отчеты о покрытии для frontend

### 2. Сборка (Build Job)
- Сборка Docker образов для backend и frontend
- Публикация в GitHub Container Registry
- Тегирование образов по версиям

### 3. Безопасность (Security Scan)
- Сканирование уязвимостей с помощью Trivy
- Загрузка результатов в GitHub Security tab

### 4. Деплой
- **Staging**: автоматический деплой при push в `develop`
- **Production**: автоматический деплой при push в `main`

## 🧪 Запуск тестов локально

### Все тесты
```bash
make test
# или
python run_tests.py
```

### Только backend
```bash
make test-backend
# или
cd backend && python -m unittest discover -s . -p "test_*.py" -v
```

### Только frontend
```bash
make test-frontend
# или
cd frontend && npm test -- --watchAll=false --coverage
```

### Интеграционные тесты
```bash
make test-integration
```

## 🔧 Настройка окружения

### Переменные окружения для тестов
```bash
# Backend тесты
DB_HOST=localhost
DB_PORT=5432
DB_NAME=books_exchange_test
DB_USER=postgres
DB_PASSWORD=postgres
```

### GitHub Secrets (для деплоя)
- `DEPLOY_SSH_KEY`: SSH ключ для сервера
- `DEPLOY_HOST`: IP адрес сервера
- `DEPLOY_USER`: пользователь для деплоя

## 📊 Отчеты о тестировании

### Покрытие кода
- Frontend: отчеты генерируются в `frontend/coverage/`
- Backend: можно добавить coverage.py для детальных отчетов

### Результаты тестов
- GitHub Actions показывает результаты в реальном времени
- Уведомления о провале тестов
- Детальные логи для отладки

## 🐳 Docker образы

### Теги образов
- `latest`: последняя версия из main
- `develop`: версия из develop ветки
- `v1.0.0`: семантические версии
- `sha-abc123`: коммит хеши

### Реестр образов
```bash
# Pull образов
docker pull ghcr.io/username/repo-backend:latest
docker pull ghcr.io/username/repo-frontend:latest
```

## 🔄 Workflow триггеры

### Автоматический запуск
- Push в `main` или `develop`
- Pull Request в `main`
- Ручной запуск через GitHub Actions

### Условный запуск
- Build job только при push в `main`
- Deploy только после успешных тестов
- Security scan для всех веток

## 🛠️ Команды Make

```bash
make help          # Показать все команды
make install       # Установить зависимости
make test          # Запустить все тесты
make build         # Собрать Docker образы
make run           # Запустить приложение
make stop          # Остановить приложение
make clean         # Очистить проект
make logs          # Показать логи
```

## 🔍 Мониторинг

### GitHub Actions
- Статус pipeline в реальном времени
- Детальные логи каждого шага
- Уведомления о результатах

### Логи приложения
```bash
make logs
# или
docker compose logs -f
```

## 🚨 Устранение неполадок

### Тесты не проходят
1. Проверить логи в GitHub Actions
2. Запустить тесты локально: `make test`
3. Проверить переменные окружения

### Сборка не удается
1. Проверить Dockerfile
2. Проверить зависимости в requirements.txt/package.json
3. Проверить права доступа к реестру

### Деплой не работает
1. Проверить SSH ключи
2. Проверить доступ к серверу
3. Проверить конфигурацию сервера

## 📈 Метрики качества

### Покрытие кода
- Frontend: минимум 70%
- Backend: можно добавить coverage.py

### Время выполнения
- Тесты: ~5-10 минут
- Сборка: ~3-5 минут
- Деплой: ~2-3 минуты

### Надежность
- Автоматический rollback при провале деплоя
- Уведомления о критических ошибках
- Мониторинг доступности сервиса

## 🔐 Безопасность

### Сканирование уязвимостей
- Trivy для Docker образов
- npm audit для frontend
- safety для Python зависимостей

### Секреты
- Все секреты хранятся в GitHub Secrets
- Никаких хардкода паролей
- Ротация ключей доступа

## 📚 Дополнительные ресурсы

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Testing Best Practices](https://martinfowler.com/articles/microservice-testing/)
- [CI/CD Best Practices](https://www.atlassian.com/continuous-delivery/principles/continuous-integration-vs-delivery-vs-deployment) 