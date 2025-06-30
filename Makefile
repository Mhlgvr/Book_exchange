.PHONY: help install test test-backend test-frontend test-integration build run stop clean

# Переменные
DOCKER_COMPOSE = docker compose
PYTHON = python3
NPM = npm

help: ## Показать справку
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Установить зависимости
	@echo "🔧 Установка зависимостей..."
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

test: ## Запустить все тесты
	@echo "🧪 Запуск всех тестов..."
	$(PYTHON) run_tests.py

test-backend: ## Запустить тесты backend
	@echo "🔧 Запуск тестов backend..."
	cd backend && $(PYTHON) -m unittest discover -s . -p "test_*.py" -v

test-frontend: ## Запустить тесты frontend
	@echo "🎨 Запуск тестов frontend..."
	cd frontend && $(NPM) test -- --watchAll=false --coverage

test-integration: ## Запустить интеграционные тесты
	@echo "🔗 Запуск интеграционных тестов..."
	$(DOCKER_COMPOSE) up -d
	@sleep 10
	cd backend && $(PYTHON) -m unittest test_api.py -v
	$(DOCKER_COMPOSE) down

build: ## Собрать Docker образы
	@echo "🐳 Сборка Docker образов..."
	$(DOCKER_COMPOSE) build

run: ## Запустить приложение
	@echo "🚀 Запуск приложения..."
	$(DOCKER_COMPOSE) up -d

stop: ## Остановить приложение
	@echo "⏹️ Остановка приложения..."
	$(DOCKER_COMPOSE) down

logs: ## Показать логи
	@echo "📋 Показать логи..."
	$(DOCKER_COMPOSE) logs -f

clean: ## Очистить проект
	@echo "🧹 Очистка проекта..."
	$(DOCKER_COMPOSE) down -v
	docker system prune -f
	rm -rf frontend/node_modules
	rm -rf frontend/build
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

dev: ## Запустить в режиме разработки
	@echo "🔧 Запуск в режиме разработки..."
	$(DOCKER_COMPOSE) -f docker-compose.yml -f docker-compose.dev.yml up -d

prod: ## Запустить в продакшн режиме
	@echo "🚀 Запуск в продакшн режиме..."
	$(DOCKER_COMPOSE) -f docker-compose.yml -f docker-compose.prod.yml up -d

lint: ## Проверить код
	@echo "🔍 Проверка кода..."
	cd backend && flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	cd frontend && $(NPM) run lint

format: ## Форматировать код
	@echo "✨ Форматирование кода..."
	cd backend && black .
	cd frontend && $(NPM) run format

security: ## Проверить безопасность
	@echo "🔒 Проверка безопасности..."
	$(DOCKER_COMPOSE) run --rm backend safety check
	cd frontend && $(NPM) audit

backup: ## Создать резервную копию БД
	@echo "💾 Создание резервной копии БД..."
	$(DOCKER_COMPOSE) exec db pg_dump -U postgres books_exchange > backup_$(shell date +%Y%m%d_%H%M%S).sql

restore: ## Восстановить БД из резервной копии
	@echo "📥 Восстановление БД..."
	@read -p "Введите имя файла резервной копии: " file; \
	$(DOCKER_COMPOSE) exec -T db psql -U postgres books_exchange < $$file 