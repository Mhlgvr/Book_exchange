-- Таблица точек обмена
CREATE TABLE IF NOT EXISTS exchange_points (
    id SERIAL PRIMARY KEY,
    address TEXT NOT NULL
);

-- Таблица книг
CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    year INTEGER NOT NULL,
    description TEXT,
    photo_url TEXT,
    point_id INTEGER REFERENCES exchange_points(id),
    user_id VARCHAR(100),
    added_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица событий
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    book_id INTEGER NOT NULL REFERENCES books(id),
    event_type TEXT NOT NULL, -- 'added' или 'taken'
    event_time TIMESTAMP NOT NULL
);

-- Вставка фиксированных точек обмена
INSERT INTO exchange_points (address) VALUES
('ул. Ленина, 1'),
('пр. Мира, 42'),
('ул. Гагарина, 7')
ON CONFLICT DO NOTHING;

-- Вставка начальных книг
INSERT INTO books (title, author, year, description, photo_url, point_id) VALUES
('Война и мир', 'Лев Толстой', 1869, 'Эпический роман о русском обществе в эпоху наполеоновских войн', 'https://tolstoy.ru/upload/creativity/fiction/detail/upload/iblock/72e/w-p.jpg', 1),
('Евгений Онегин', 'Александр Пушкин', 1833, 'Роман в стихах о любви и судьбе', 'https://cdn.azbooka.ru/cv/w1100/8fb16b40-17d4-43fa-b3fa-20238b342ad3.jpg', 2),
('Анна Каренина', 'Лев Толстой', 1877, 'Роман о любви, браке и общественных нормах', 'https://cdn.azbooka.ru/cv/w1100/2be65e41-13fb-4f97-b337-8c178a9e5d92.jpg', 3),
('Герой нашего времени', 'Михаил Лермонтов', 1840, 'Психологический роман о Печорине и его времени', 'https://cdn.azbooka.ru/cv/w1100/5061fd29-00b3-4776-b247-35382c535628.jpg', 1),
('Отцы и дети', 'Иван Тургенев', 1862, 'Роман о конфликте поколений и нигилизме', 'https://cdn.azbooka.ru/cv/w1100/2be65e41-13fb-4f97-b337-8c178a9e5d92.jpg', 2)
ON CONFLICT DO NOTHING; 