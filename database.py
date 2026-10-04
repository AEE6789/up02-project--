"""
Мой модуль-посредник (драйвер) для подключения к SQLite.
Разработчик: mawr89-rgb
Вариант: 20
Дата: 04.10.2026
"""
import sqlite3
import os

# ⚠️ Указываю точный путь к базе данных с учётом папки databases
DB_PATH = "databases/db_variant_20.db"


def get_all_products():
    """
    Вытаскиваю все строки из таблицы 'Товар'.
    Возвращаю список кортежей, чтобы файл каталога мог их отрисовать.
    """
    # Проверяю, лежит ли файл бд в папке databases, чтобы прога не крашнулась
    if not os.path.exists(DB_PATH):
        print(f"⚠️ ОШИБКА: Не вижу файл '{DB_PATH}'. Проверь имя папки и файла!")
        return []
        
    # Подключаюсь к своей базе данных
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        
        cursor.execute("SELECT id, категория, название, состав, цена, количество, фото FROM Товар")
        products = cursor.fetchall()
        return products
        
    except sqlite3.OperationalError as e:
        
        print(f"⚠️ Косяк в SQL-запросе: {e}")
        print("Надо проверить, что таблица в БД реально называется 'Товар'.")
        return []
        
    finally:
        conn.close()
