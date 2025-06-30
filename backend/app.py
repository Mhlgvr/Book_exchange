from __init__ import app
import db

if __name__ == "__main__":
    # Инициализируем базу данных при запуске приложения
    with app.app_context():
        db.init_db()
    app.run(host="0.0.0.0", port=5001, debug=True) 