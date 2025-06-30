import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import '@testing-library/jest-dom';
import App from './App';

// Mock fetch для тестирования API вызовов
global.fetch = jest.fn();

// Mock alert для тестов
global.alert = jest.fn();

describe('App Component', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  test('renders header with title', async () => {
    // Мокаем успешные API вызовы
    fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      });

    await act(async () => {
      render(<App />);
    });

    await waitFor(() => {
      expect(screen.getByText('📚 Сервис обмена книгами')).toBeInTheDocument();
    });
  });

  test('renders "Мои книги" button', async () => {
    // Мокаем успешные API вызовы
    fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      });

    await act(async () => {
      render(<App />);
    });

    await waitFor(() => {
      expect(screen.getByText('Мои книги')).toBeInTheDocument();
    });
  });

  test('renders "Добавить книгу" button', async () => {
    // Мокаем успешные API вызовы
    fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      });

    await act(async () => {
      render(<App />);
    });

    await waitFor(() => {
      expect(screen.getByText('Добавить книгу')).toBeInTheDocument();
    });
  });

  test('shows loading state initially', () => {
    // Не мокаем fetch, чтобы показать состояние загрузки
    render(<App />);
    expect(screen.getByText('Загрузка...')).toBeInTheDocument();
  });

  test('displays books after successful API call', async () => {
    const mockBooks = [
      {
        id: 1,
        title: 'Тестовая книга',
        author: 'Тестовый автор',
        year: 2024,
        description: 'Описание',
        user_id: null,
        point_id: 1
      }
    ];

    const mockPoints = [
      { id: 1, address: 'Тестовая точка' }
    ];

    fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockBooks
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockPoints
      });

    await act(async () => {
      render(<App />);
    });

    await waitFor(() => {
      expect(screen.getByText('Тестовая книга')).toBeInTheDocument();
    });
  });

  test('shows error message when API call fails', async () => {
    fetch.mockRejectedValueOnce(new Error('API Error'));

    await act(async () => {
      render(<App />);
    });

    await waitFor(() => {
      expect(screen.getByText('Ошибка загрузки данных')).toBeInTheDocument();
    });
  });

  test('opens add book form when button is clicked', async () => {
    // Мокаем успешные API вызовы
    fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      });

    await act(async () => {
      render(<App />);
    });

    await waitFor(() => {
      const addButton = screen.getByText('Добавить книгу');
      fireEvent.click(addButton);
    });
    
    expect(screen.getByText('Добавить свою книгу')).toBeInTheDocument();
  });

  test('switches to "Мои книги" view when button is clicked', async () => {
    const mockMyBooks = [
      {
        id: 1,
        title: 'Моя книга',
        author: 'Мой автор',
        year: 2024,
        user_id: null,
        added_by: 'user_1'
      }
    ];

    fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockMyBooks
      });

    await act(async () => {
      render(<App />);
    });

    await waitFor(() => {
      const myBooksButton = screen.getByText('Мои книги');
      fireEvent.click(myBooksButton);
    });

    await waitFor(() => {
      expect(screen.getByText('Моя книга')).toBeInTheDocument();
    });
  });

  test('renders admin button', async () => {
    fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      });

    await act(async () => {
      render(<App />);
    });

    await waitFor(() => {
      expect(screen.getByText('🔐 Админ')).toBeInTheDocument();
    });
  });

  test('opens admin login form when admin button is clicked', async () => {
    fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      });

    await act(async () => {
      render(<App />);
    });

    await waitFor(() => {
      const adminButton = screen.getByText('🔐 Админ');
      fireEvent.click(adminButton);
    });

    expect(screen.getByText('🔐 Вход в админ панель')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Введите пароль')).toBeInTheDocument();
  });

  test('successful admin login', async () => {
    fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Успешная аутентификация', token: 'admin_token_123' })
      });

    await act(async () => {
      render(<App />);
    });

    await waitFor(() => {
      const adminButton = screen.getByText('🔐 Админ');
      fireEvent.click(adminButton);
    });

    const passwordInput = screen.getByPlaceholderText('Введите пароль');
    const loginButton = screen.getByText('Войти');

    await act(async () => {
      fireEvent.change(passwordInput, { target: { value: 'admin' } });
      fireEvent.click(loginButton);
    });

    await waitFor(() => {
      expect(screen.getByText('👨‍💼 Админ панель')).toBeInTheDocument();
    });
  });

  test('failed admin login', async () => {
    fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })
      .mockResolvedValueOnce({
        ok: false,
        status: 401
      });

    await act(async () => {
      render(<App />);
    });

    await waitFor(() => {
      const adminButton = screen.getByText('🔐 Админ');
      fireEvent.click(adminButton);
    });

    const passwordInput = screen.getByPlaceholderText('Введите пароль');
    const loginButton = screen.getByText('Войти');

    await act(async () => {
      fireEvent.change(passwordInput, { target: { value: 'wrong_password' } });
      fireEvent.click(loginButton);
    });

    // Проверяем, что форма все еще видна (не закрылась)
    expect(screen.getByText('🔐 Вход в админ панель')).toBeInTheDocument();
  });

  test('admin logout', async () => {
    fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Успешная аутентификация', token: 'admin_token_123' })
      });

    await act(async () => {
      render(<App />);
    });

    await waitFor(() => {
      const adminButton = screen.getByText('🔐 Админ');
      fireEvent.click(adminButton);
    });

    const passwordInput = screen.getByPlaceholderText('Введите пароль');
    const loginButton = screen.getByText('Войти');

    await act(async () => {
      fireEvent.change(passwordInput, { target: { value: 'admin' } });
      fireEvent.click(loginButton);
    });

    await waitFor(() => {
      const logoutButton = screen.getByText('🚪 Выход');
      fireEvent.click(logoutButton);
    });

    // Проверяем, что админ панель исчезла
    expect(screen.queryByText('👨‍💼 Админ панель')).not.toBeInTheDocument();
  });

  test('add book form functionality', async () => {
    fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => []
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => [{ id: 1, address: 'Точка 1' }]
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Книга успешно добавлена', book_id: 1 })
      });

    await act(async () => {
      render(<App />);
    });

    await waitFor(() => {
      const addButton = screen.getByText('Добавить книгу');
      fireEvent.click(addButton);
    });

    // Проверяем, что форма отображается
    expect(screen.getByText('Добавить свою книгу')).toBeInTheDocument();
    expect(screen.getByText('Название книги *:')).toBeInTheDocument();
    expect(screen.getByText('Автор *:')).toBeInTheDocument();
    expect(screen.getByText('Год издания *:')).toBeInTheDocument();
    expect(screen.getByText('Точка обмена *:')).toBeInTheDocument();
  });

  test('take book functionality', async () => {
    const mockBooks = [
      {
        id: 1,
        title: 'Доступная книга',
        author: 'Автор',
        year: 2024,
        user_id: null,
        point_id: 1
      }
    ];

    const mockUpdatedBooks = [
      {
        id: 1,
        title: 'Доступная книга',
        author: 'Автор',
        year: 2024,
        user_id: 'user_1', // Книга теперь забрана
        point_id: 1
      }
    ];

    fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockBooks
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => [{ id: 1, address: 'Точка 1' }]
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Книга успешно забрана' })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockUpdatedBooks
      });

    await act(async () => {
      render(<App />);
    });

    await waitFor(() => {
      const takeButton = screen.getByText('Забрать книгу');
      fireEvent.click(takeButton);
    });

    // Проверяем, что кнопка исчезла после взятия книги
    await waitFor(() => {
      expect(screen.queryByText('Забрать книгу')).not.toBeInTheDocument();
    });
  });

  test('filter functionality', async () => {
    const mockBooks = [
      {
        id: 1,
        title: 'Книга 1',
        author: 'Автор 1',
        year: 2020,
        point_id: 1
      },
      {
        id: 2,
        title: 'Книга 2',
        author: 'Автор 2',
        year: 2021,
        point_id: 2
      }
    ];

    fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockBooks
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => [{ id: 1, address: 'Точка 1' }, { id: 2, address: 'Точка 2' }]
      });

    await act(async () => {
      render(<App />);
    });

    await waitFor(() => {
      const authorFilter = screen.getByPlaceholderText('Введите автора');
      const applyButton = screen.getByText('Применить');
      
      fireEvent.change(authorFilter, { target: { value: 'Автор 1' } });
      fireEvent.click(applyButton);
    });

    // Проверяем, что фильтр применился
    expect(screen.getByDisplayValue('Автор 1')).toBeInTheDocument();
  });
}); 