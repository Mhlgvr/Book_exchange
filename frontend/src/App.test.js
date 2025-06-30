import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';

// Mock fetch для тестирования API вызовов
global.fetch = jest.fn();

describe('App Component', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  test('renders header with title', () => {
    render(<App />);
    expect(screen.getByText('📚 Сервис обмена книгами')).toBeInTheDocument();
  });

  test('renders "Мои книги" button', () => {
    render(<App />);
    expect(screen.getByText('Мои книги')).toBeInTheDocument();
  });

  test('renders "Добавить книгу" button', () => {
    render(<App />);
    expect(screen.getByText('Добавить книгу')).toBeInTheDocument();
  });

  test('shows loading state initially', () => {
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

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText('Тестовая книга')).toBeInTheDocument();
    });
  });

  test('shows error message when API call fails', async () => {
    fetch.mockRejectedValueOnce(new Error('API Error'));

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText('Ошибка загрузки данных')).toBeInTheDocument();
    });
  });

  test('opens add book form when button is clicked', () => {
    render(<App />);
    
    const addButton = screen.getByText('Добавить книгу');
    fireEvent.click(addButton);
    
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

    render(<App />);

    await waitFor(() => {
      const myBooksButton = screen.getByText('Мои книги');
      fireEvent.click(myBooksButton);
    });

    await waitFor(() => {
      expect(screen.getByText('Моя книга')).toBeInTheDocument();
    });
  });
}); 