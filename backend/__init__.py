from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Загружаем переменные окружения
load_dotenv()

app = Flask(__name__)
CORS(app)

# Настройки Flask из переменных окружения
app.config['ENV'] = os.getenv('FLASK_ENV', 'development')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'True')

import routes
import db

# Инициализация базы данных будет выполнена при необходимости
# (например, в тестах или при запуске приложения)

__all__ = ['app'] 