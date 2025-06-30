import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [books, setBooks] = useState([]);
  const [points, setPoints] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    point_id: '',
    author: '',
    title: '',
    year: ''
  });
  const [showAddForm, setShowAddForm] = useState(false);
  const [showMyBooks, setShowMyBooks] = useState(false);
  const [myBooks, setMyBooks] = useState([]);
  const [newBook, setNewBook] = useState({
    title: '',
    author: '',
    year: '',
    description: '',
    photo_url: '',
    point_id: ''
  });
  const [error, setError] = useState(null);

  // Загрузка данных при монтировании компонента
  useEffect(() => {
    fetchBooks();
    fetchPoints();
  }, []);

  // Загрузка книг
  const fetchBooks = async () => {
    try {
      setError(null);
      const params = new URLSearchParams();
      if (filters.author) params.append('author', filters.author);
      if (filters.title) params.append('title', filters.title);
      if (filters.point_id) params.append('point_id', filters.point_id);

      const response = await fetch(`http://localhost:5001/api/books?${params}`);
      const data = await response.json();
      setBooks(data);
    } catch (error) {
      console.error('Ошибка загрузки книг:', error);
      setError('Ошибка загрузки данных');
    } finally {
      setLoading(false);
    }
  };

  // Загрузка точек обмена
  const fetchPoints = async () => {
    try {
      const response = await fetch('http://localhost:5001/api/points');
      const data = await response.json();
      setPoints(data);
    } catch (error) {
      console.error('Ошибка загрузки точек обмена:', error);
    }
  };

  // Обработка изменения фильтров
  const handleFilterChange = (field, value) => {
    setFilters(prev => ({ ...prev, [field]: value }));
  };

  // Применение фильтров
  const applyFilters = () => {
    fetchBooks();
  };

  // Забрать книгу
  const takeBook = async (bookId) => {
    try {
      const response = await fetch(`http://localhost:5001/api/books/${bookId}/take`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        alert('Книга успешно забрана!');
        // Обновляем список книг
        fetchBooks();
      } else {
        const error = await response.json();
        alert(`Ошибка: ${error.message || 'Не удалось забрать книгу'}`);
      }
    } catch (error) {
      console.error('Ошибка при взятии книги:', error);
      alert('Ошибка при взятии книги');
    }
  };

  // Получить мои книги
  const fetchMyBooks = async () => {
    try {
      const response = await fetch('http://localhost:5001/api/books/my');
      if (response.ok) {
        const data = await response.json();
        setMyBooks(data);
      } else {
        console.error('Ошибка при получении моих книг');
      }
    } catch (error) {
      console.error('Ошибка при получении моих книг:', error);
    }
  };

  // Добавить книгу
  const addBook = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5001/api/books/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newBook)
      });
      
      if (response.ok) {
        alert('Книга успешно добавлена!');
        setShowAddForm(false);
        setNewBook({
          title: '',
          author: '',
          year: '',
          description: '',
          photo_url: '',
          point_id: ''
        });
        // Обновляем списки книг
        fetchBooks();
        fetchMyBooks();
      } else {
        const error = await response.json();
        alert(`Ошибка: ${error.message || 'Не удалось добавить книгу'}`);
      }
    } catch (error) {
      console.error('Ошибка при добавлении книги:', error);
      alert('Ошибка при добавлении книги');
    }
  };

  // Обработчик изменения полей формы
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewBook(prev => ({
      ...prev,
      [name]: value
    }));
  };

  if (loading) {
    return <div className="App">Загрузка...</div>;
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>📚 Сервис обмена книгами</h1>
        <div className="header-buttons">
          <button 
            className="header-btn"
            onClick={() => {
              setShowMyBooks(!showMyBooks);
              if (!showMyBooks) {
                fetchMyBooks();
              }
            }}
          >
            {showMyBooks ? 'Все книги' : 'Мои книги'}
          </button>
          <button 
            className="header-btn"
            onClick={() => setShowAddForm(!showAddForm)}
          >
            {showAddForm ? 'Отмена' : 'Добавить книгу'}
          </button>
        </div>
      </header>

      {/* Форма добавления книги */}
      {showAddForm && (
        <div className="add-book-form">
          <h2>Добавить свою книгу</h2>
          <form onSubmit={addBook}>
            <div className="form-row">
              <div className="form-group">
                <label>Название книги *:</label>
                <input
                  type="text"
                  name="title"
                  value={newBook.title}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Автор *:</label>
                <input
                  type="text"
                  name="author"
                  value={newBook.author}
                  onChange={handleInputChange}
                  required
                />
              </div>
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Год издания *:</label>
                <input
                  type="number"
                  name="year"
                  value={newBook.year}
                  onChange={handleInputChange}
                  min="1800"
                  max="2025"
                  required
                />
              </div>
              <div className="form-group">
                <label>Точка обмена *:</label>
                <select
                  name="point_id"
                  value={newBook.point_id}
                  onChange={handleInputChange}
                  required
                >
                  <option value="">Выберите точку обмена</option>
                  {points.map(point => (
                    <option key={point.id} value={point.id}>
                      {point.address}
                    </option>
                  ))}
                </select>
              </div>
            </div>
            <div className="form-group">
              <label>Описание:</label>
              <textarea
                name="description"
                value={newBook.description}
                onChange={handleInputChange}
                rows="3"
              />
            </div>
            <div className="form-group">
              <label>URL обложки:</label>
              <input
                type="url"
                name="photo_url"
                value={newBook.photo_url}
                onChange={handleInputChange}
                placeholder="https://example.com/cover.jpg"
              />
            </div>
            <div className="form-actions">
              <button type="submit" className="submit-btn">Добавить книгу</button>
              <button 
                type="button" 
                className="cancel-btn"
                onClick={() => setShowAddForm(false)}
              >
                Отмена
              </button>
            </div>
          </form>
        </div>
      )}

      <main className="App-main">
        {/* Отображение ошибки */}
        {error && (
          <div className="error-message" style={{ 
            backgroundColor: '#ffebee', 
            color: '#c62828', 
            padding: '10px', 
            margin: '10px 0', 
            borderRadius: '4px',
            border: '1px solid #ef5350'
          }}>
            {error}
          </div>
        )}
        
        {/* Фильтры */}
        {!showMyBooks && (
          <div className="filters">
            <h2>Фильтры</h2>
            <div className="filter-row">
              <div className="filter-group">
                <label>Точка обмена:</label>
                <select
                  value={filters.point_id}
                  onChange={(e) => setFilters({...filters, point_id: e.target.value})}
                >
                  <option value="">Все точки</option>
                  {points.map(point => (
                    <option key={point.id} value={point.id}>
                      {point.address}
                    </option>
                  ))}
                </select>
              </div>
              <div className="filter-group">
                <label>Автор:</label>
                <input
                  type="text"
                  value={filters.author}
                  onChange={(e) => setFilters({...filters, author: e.target.value})}
                  placeholder="Введите автора"
                />
              </div>
              <div className="filter-group">
                <label>Название:</label>
                <input
                  type="text"
                  value={filters.title}
                  onChange={(e) => setFilters({...filters, title: e.target.value})}
                  placeholder="Введите название"
                />
              </div>
              <div className="filter-group">
                <label>Год:</label>
                <input
                  type="number"
                  value={filters.year}
                  onChange={(e) => setFilters({...filters, year: e.target.value})}
                  placeholder="Год издания"
                />
              </div>
              <button onClick={applyFilters} className="apply-btn">Применить</button>
            </div>
          </div>
        )}

        {/* Список книг */}
        <div className="books-container">
          <h2>{showMyBooks ? 'Мои книги' : 'Все доступные книги'}</h2>
          {showMyBooks ? (
            myBooks.length > 0 ? (
              <div className="books-grid">
                {myBooks.map(book => (
                  <div key={book.id} className="book-card my-book">
                    <img 
                      src={book.photo_url || 'https://via.placeholder.com/150x200/cccccc/666666?text=Книга'} 
                      alt={book.title}
                      className="book-cover"
                      onError={(e) => {
                        e.target.src = 'https://via.placeholder.com/150x200/cccccc/666666?text=Книга';
                      }}
                    />
                    <div className="book-info">
                      <h3>{book.title}</h3>
                      <p><strong>Автор:</strong> {book.author}</p>
                      <p><strong>Год:</strong> {book.year}</p>
                      <p><strong>Описание:</strong> {book.description}</p>
                      <p><strong>Точка обмена:</strong> {points.find(p => p.id === book.point_id)?.address}</p>
                      <p className="book-status">
                        <strong>Статус:</strong> 
                        <span className="my-book-status">
                          {book.user_id ? 'Забрана мной' : 'Добавлена мной'}
                        </span>
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="no-books">У вас пока нет добавленных книг</p>
            )
          ) : (
            books.length > 0 ? (
              <div className="books-grid">
                {books.map(book => (
                  <div key={book.id} className="book-card">
                    <img 
                      src={book.photo_url || 'https://via.placeholder.com/150x200/cccccc/666666?text=Книга'} 
                      alt={book.title}
                      className="book-cover"
                      onError={(e) => {
                        console.log('Ошибка загрузки изображения для книги:', book.title);
                        e.target.src = 'https://via.placeholder.com/150x200/cccccc/666666?text=Книга';
                      }}
                    />
                    <div className="book-info">
                      <h3>{book.title}</h3>
                      <p><strong>Автор:</strong> {book.author}</p>
                      <p><strong>Год:</strong> {book.year}</p>
                      <p><strong>Описание:</strong> {book.description}</p>
                      <p><strong>Точка обмена:</strong> {points.find(p => p.id === book.point_id)?.address}</p>
                      <p className="book-status">
                        <strong>Статус:</strong> 
                        <span className={book.user_id ? 'taken' : 'available'}>
                          {book.user_id ? 'Забрана' : 'Доступна'}
                        </span>
                      </p>
                    </div>
                    {!book.user_id && (
                      <button onClick={() => takeBook(book.id)}>Забрать книгу</button>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <p className="no-books">Книги не найдены</p>
            )
          )}
        </div>

        {/* Информация о сервисе */}
        <section className="info">
          <h2>ℹ️ О сервисе</h2>
          <p>Это учебный проект сервиса обмена книгами с REST API на Flask и SPA интерфейсом на React.</p>
          <p><strong>API документация:</strong> <a href="http://localhost:5001/apidocs/" target="_blank" rel="noopener noreferrer">Swagger UI</a></p>
        </section>
      </main>
    </div>
  );
}

export default App;
