import psycopg
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Формируем DSN из переменных окружения
DSN = f"dbname={os.getenv('DB_NAME', 'books_exchange')} user={os.getenv('DB_USER', 'postgres')} password={os.getenv('DB_PASSWORD', 'postgres')} host={os.getenv('DB_HOST', 'db')} port={os.getenv('DB_PORT', '5432')}"

def get_db():
    conn = psycopg.connect(DSN)
    conn.row_factory = psycopg.rows.dict_row
    return conn

def init_db():
    """Инициализация базы данных - создание таблиц и начальных данных"""
    conn = get_db()
    with conn.cursor() as cur:
        # Проверяем, существует ли уже таблица books
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'books'
            );
        """)
        table_exists = cur.fetchone()['exists']
        
        if not table_exists:
            # Читаем SQL файл только если таблицы не существуют
            with open('models.sql', 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            # Выполняем SQL команды
            cur.execute(sql_content)
            conn.commit()
            print("База данных инициализирована успешно")
        else:
            print("База данных уже инициализирована")

def get_exchange_points():
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM exchange_points;")
        return cur.fetchall()

def add_book(title, author, year, description, photo_url, point_id, user_id, added_by=None):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO books (title, author, year, description, photo_url, point_id, user_id, added_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
            """,
            (title, author, year, description, photo_url, point_id, user_id, added_by)
        )
        result = cur.fetchone()
        book_id = result['id']
        conn.commit()
        return book_id

def get_books(filters = None):
    conn = get_db()
    query = "SELECT * FROM books WHERE TRUE"
    params = []
    if filters:
        if 'point_id' in filters:
            query += " AND point_id = %s"
            params.append(filters['point_id'])
        if 'author' in filters:
            query += " AND author ILIKE %s"
            params.append(f"%{filters['author']}%")
        if 'title' in filters:
            query += " AND title ILIKE %s"
            params.append(f"%{filters['title']}%")
        if 'year' in filters:
            query += " AND year = %s"
            params.append(filters['year'])
    with conn.cursor() as cur:
        cur.execute(query, params)
        return cur.fetchall()
    
def get_book(book_id):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM books WHERE id = %s;", (book_id,))
        return cur.fetchone()
    
def take_book(book_id, user_id):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("UPDATE books SET user_id = %s WHERE id = %s;", (user_id, book_id))
        conn.commit()


def get_user_books(user_id):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM books WHERE added_by = %s ORDER BY created_at DESC;", (user_id,))
        return cur.fetchall()

# --- Журнал событий ---
def log_event(book_id, event_type):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO events (book_id, event_type, event_time)
            VALUES (%s, %s, NOW());
            """,
            (book_id, event_type)
        )
        conn.commit()

def get_events():
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT e.id, e.book_id, b.title, e.event_type, e.event_time
            FROM events e
            JOIN books b ON e.book_id = b.id
            ORDER BY e.event_time DESC;
            """
        )
        return cur.fetchall() 