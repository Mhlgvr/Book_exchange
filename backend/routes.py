from flask import request, jsonify
from __init__ import app
import db as db_layer

from flasgger import Swagger
swagger = Swagger(app)

@app.route('/api/points', methods=['GET'])
def get_points():
    """
    Получить список точек обмена
    ---
    tags:
      - Точки обмена
    responses:
      200:
        description: Список точек обмена
    """
    points = db_layer.get_exchange_points()
    return jsonify(points)

@app.route('/api/books', methods=['GET'])
def get_books():
    """
    Получить список книг с фильтрами
    ---
    tags:
      - Книги
    parameters:
      - name: point_id
        in: query
        type: integer
        required: false
      - name: author
        in: query
        type: string
        required: false
      - name: title
        in: query
        type: string
        required: false
      - name: year
        in: query
        type: integer
        required: false
    responses:
      200:
        description: Список книг
    """
    filters = {}
    for key in ['point_id', 'author', 'title', 'year']:
        value = request.args.get(key)
        if value:
            filters[key] = value
    books = db_layer.get_books(filters)
    return jsonify(books)

@app.route('/api/books/user/<user_id>', methods=['GET'])
def get_user_books(user_id):
    """
    Получить список книг пользователя
    ---
    tags:
      - Книги
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Список книг пользователя
    """
    books = db_layer.get_user_books(user_id)
    return jsonify(books)

@app.route('/api/admin/books', methods=['GET'])
def admin_books():
    """
    Получить все загруженные книги (админ)
    ---
    tags:
      - Админ
    responses:
      200:
        description: Список всех книг
    """
    books = db_layer.get_books()
    return jsonify(books)

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    """
    Аутентификация админа
    ---
    tags:
      - Админ
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            password:
              type: string
              required: true
    responses:
      200:
        description: Успешная аутентификация
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Успешная аутентификация"
            token:
              type: string
              example: "admin_token_123"
      401:
        description: Неверный пароль
    """
    try:
        data = request.json
        password = data.get('password')
        
        if password == 'admin':
            return jsonify({
                'message': 'Успешная аутентификация',
                'token': 'admin_token_123'
            }), 200
        else:
            return jsonify({'message': 'Неверный пароль'}), 401
            
    except Exception as e:
        return jsonify({'message': f'Ошибка сервера: {str(e)}'}), 500

@app.route('/api/admin/events', methods=['GET'])
def admin_events():
    """
    Получить журнал событий (админ)
    ---
    tags:
      - Админ
    responses:
      200:
        description: Журнал событий
    """
    events = db_layer.get_events()
    return jsonify(events)

@app.route('/api/books/<int:book_id>/take', methods=['POST'])
def take_book(book_id):
    """
    Забрать книгу
    ---
    tags:
      - Книги
    parameters:
      - name: book_id
        in: path
        type: integer
        required: true
        description: ID книги
    responses:
      200:
        description: Книга успешно забрана
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Книга успешно забрана"
      404:
        description: Книга не найдена
      400:
        description: Книга уже забрана
    """
    try:
        book = db_layer.get_book(book_id)
        if not book:
            return jsonify({'message': 'Книга не найдена'}), 404
        
        # Проверяем, не забрана ли уже книга
        if book['user_id'] is not None:
            return jsonify({'message': 'Книга уже забрана'}), 400
        
        # Забираем книгу (используем фиксированный user_id)
        db_layer.take_book(book_id, 'user_1')
        db_layer.log_event(book_id, 'taken')
            
        return jsonify({'message': 'Книга успешно забрана'}), 200
            
    except Exception as e:
        return jsonify({'message': f'Ошибка сервера: {str(e)}'}), 500 

@app.route('/api/books/add', methods=['POST'])
def add_user_book():
    """
    Добавить свою книгу
    ---
    tags:
      - Книги
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            title:
              type: string
              required: true
            author:
              type: string
              required: true
            year:
              type: integer
              required: true
            description:
              type: string
            photo_url:
              type: string
            point_id:
              type: integer
              required: true
    responses:
      201:
        description: Книга добавлена
      400:
        description: Неверные данные
    """
    try:
        data = request.json
        
        # Проверяем обязательные поля
        required_fields = ['title', 'author', 'year', 'point_id']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'message': f'Поле {field} обязательно'}), 400
        
        # Добавляем книгу с user_id = None (книга доступна для взятия)
        book_id = db_layer.add_book(
            data['title'],
            data['author'],
            data['year'],
            data.get('description', 'Описание отсутствует'),
            data.get('photo_url', 'https://via.placeholder.com/300x400/cccccc/666666?text=Книга'),
            data['point_id'],
            None,  # Книга доступна для взятия
            'user_1'  # Кто добавил книгу
        )
        
        # Логируем событие
        db_layer.log_event(book_id, 'added_by_user')
        
        return jsonify({'message': 'Книга успешно добавлена', 'book_id': book_id}), 201
        
    except Exception as e:
        return jsonify({'message': f'Ошибка сервера: {str(e)}'}), 500

@app.route('/api/books/my', methods=['GET'])
def get_my_books():
    """
    Получить мои книги
    ---
    tags:
      - Книги
    responses:
      200:
        description: Список моих книг
    """
    try:
        books = db_layer.get_user_books('user_1')
        return jsonify(books)
    except Exception as e:
        return jsonify({'message': f'Ошибка сервера: {str(e)}'}), 500 