"""Работа с заказами для Варианта №20 (Кулинария)."""
import sqlite3
from datetime import datetime
from config import DB_PATH

def get_connection():
    """Устанавливает соединение с БД кулинарии."""
    return sqlite3.connect(DB_PATH)

def add_order_to_db(client, product_id, quantity):
    """
    Добавляет новый заказ в таблицу 'Заказ'.
    Строго соответствует полям: дата, клиент, товар_id, количество.
    """
    conn = get_connection()
    cur = conn.cursor()
    
    # Форматирование даты согласно системным записям в вашей БД (ГГГГ-ММ-ДД)
    дата = datetime.now().strftime("%Y-%m-%d")
    
    # Имена столбцов взяты точь-в-точь со скриншота таблицы "Заказ"
    cur.execute(
        "INSERT INTO Заказ (дата, клиент, товар_id, количество) VALUES (?, ?, ?, ?)",
        (дата, client, product_id, quantity)
    )
    
    conn.commit()
    order_id = cur.lastrowid  # Получение автоинкрементного id
    conn.close()
    return order_id

def update_product_quantity(product_id, new_quantity):
    """
    Обновляет количество блюда на кухне в таблице 'Товар'.
    """
    conn = get_connection()
    cur = conn.cursor()
    
    # Поле 'количество' и 'id' полностью соответствуют вашей таблице "Товар"
    cur.execute(
        "UPDATE Товар SET количество = ? WHERE id = ?",
        (new_quantity, product_id)
    )
    
    conn.commit()
    conn.close()

def get_last_order_id():
    """
    Возвращает id самого последнего созданного заказа.
    """
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT MAX(id) FROM Заказ")
    row = cur.fetchone()
    conn.close()
    
    return row[0] if row and row[0] is not None else None

def get_product_quantity(product_id):
    """
    Возвращает текущий остаток порций блюда по его id.
    """
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT количество FROM Товар WHERE id = ?", (product_id,))
    row = cur.fetchone()
    conn.close()
    
    return row[0] if row else 0
