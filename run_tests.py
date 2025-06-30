#!/usr/bin/env python3
"""
Скрипт для запуска всех тестов проекта
"""

import subprocess
import sys
import os

def run_backend_tests():
    """Запуск тестов backend"""
    print("🔧 Запуск тестов backend...")
    try:
        result = subprocess.run([
            sys.executable, '-m', 'unittest', 'discover', '-s', 'backend', '-p', 'test_*.py', '-v'
        ], cwd='backend', capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Тесты backend прошли успешно")
            print(result.stdout)
        else:
            print("❌ Тесты backend провалились")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Ошибка запуска тестов backend: {e}")
        return False
    return True

def run_frontend_tests():
    """Запуск тестов frontend"""
    print("🎨 Запуск тестов frontend...")
    try:
        result = subprocess.run([
            'npm', 'test', '--', '--watchAll=false', '--coverage'
        ], cwd='frontend', capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Тесты frontend прошли успешно")
            print(result.stdout)
        else:
            print("❌ Тесты frontend провалились")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Ошибка запуска тестов frontend: {e}")
        return False
    return True

def run_integration_tests():
    """Запуск интеграционных тестов"""
    print("🔗 Запуск интеграционных тестов...")
    try:
        # Запускаем контейнеры для тестирования
        subprocess.run(['docker', 'compose', 'up', '-d'], check=True)
        
        # Ждем запуска сервисов
        import time
        time.sleep(10)
        
        # Запускаем тесты API
        result = subprocess.run([
            sys.executable, '-m', 'unittest', 'test_api.py', '-v'
        ], cwd='backend', capture_output=True, text=True)
        
        # Останавливаем контейнеры
        subprocess.run(['docker', 'compose', 'down'], check=True)
        
        if result.returncode == 0:
            print("✅ Интеграционные тесты прошли успешно")
            print(result.stdout)
        else:
            print("❌ Интеграционные тесты провалились")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Ошибка запуска интеграционных тестов: {e}")
        return False
    return True

def main():
    """Главная функция"""
    print("🚀 Запуск всех тестов проекта")
    print("=" * 50)
    
    success = True
    
    # Запуск unit тестов backend
    if not run_backend_tests():
        success = False
    
    # Запуск тестов frontend
    if not run_frontend_tests():
        success = False
    
    # Запуск интеграционных тестов
    if not run_integration_tests():
        success = False
    
    print("=" * 50)
    if success:
        print("🎉 Все тесты прошли успешно!")
        sys.exit(0)
    else:
        print("💥 Некоторые тесты провалились!")
        sys.exit(1)

if __name__ == '__main__':
    main() 