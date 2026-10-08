"""Работа с заказами для Варианта №20 (Кулинария)."""
import sqlite3
from datetime import datetime
from config import DB_PATH

def get_connection():
    """Устанавливает соединение с БД кулинарии."""
    return sqlite3.connect(DB_PATH)


# === ЗАДАНИЕ 5.2: ОБНОВЛЕНИЕ ADD_ORDER_TO_DB С ХИТРОСТЬЮ ДЛЯ NOT NULL ===
def add_order_to_db(client, date=None):
    """
    Добавляет новый заказ в БД.
    :param client: ФИО клиента
    :param date: дата заказа (по умолчанию — сегодня)
    :return: id заказа или None при ошибке
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    conn = get_connection()
    cur = conn.cursor()

    # Передаем 0 в старые столбцы товар_id и количество, чтобы обойти ошибку NOT NULL
    cur.execute(
        "INSERT INTO Заказ (дата, клиент, товар_id, количество) VALUES (?, ?, ?, ?)",
        (date, client, 0, 0)
    )
    conn.commit()
    order_id = cur.lastrowid
    conn.close()

    return order_id


# === ЗАДАНИЕ 6.2: РЕАЛИЗАЦИЯ INSERT В «СОСТАВ_ЗАКАЗА» ===
def add_order_item(order_id, product_id, size, quantity, price):
    """
    Добавляет позицию в состав заказа.
    :param order_id: id заказа
    :param product_id: id товара
    :param size: размер
    :param quantity: количество
    :param price: цена за единицу на момент заказа
    :return: id позиции или None
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO Состав_заказа "
        "(заказ_id, товар_id, размер, количество, цена) "
        "VALUES (?, ?, ?, ?, ?)",
        (order_id, product_id, size, quantity, price)
    )
    conn.commit()
    item_id = cur.lastrowid
    conn.close()

    return item_id


# === ЗАДАНИЕ 6.4: КОМПЛЕКСНАЯ ФУНКЦИЯ CREATE_ORDER ===
def create_order(client, items):
    """
    Создаёт заказ с несколькими позициями.
    :param client: ФИО клиента
    :param items: список кортежей (product_id, size, quantity, price)
    :return: id заказа
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        # 1. Создаём заказ (передаем заглушки 0, 0 для совместимости)
        date = datetime.now().strftime("%Y-%m-%d")
        cur.execute(
            "INSERT INTO Заказ (дата, клиент, товар_id, количество) VALUES (?, ?, ?, ?)",
            (date, client, 0, 0)
        )
        order_id = cur.lastrowid

        # 2. Добавляем позиции в новую таблицу Состав_заказа
        for product_id, size, quantity, price in items:
            cur.execute(
                "INSERT INTO Состав_заказа "
                "(заказ_id, товар_id, размер, количество, цена) "  # ИСПРАВЛЕНО: строго 'цена'
                "VALUES (?, ?, ?, ?, ?)",
                (order_id, product_id, size, quantity, price)
            )

        # 3. Фиксируем изменения
        conn.commit()
        return order_id

    except Exception as e:
        conn.rollback()
        print(f"Ошибка создания заказа: {e}")
        return None

    finally:
        conn.close()


# === МЕТОДЫ ПРОШЛЫХ ПАР ДЛЯ СТАБИЛЬНОСТИ СИСТЕМЫ ===
def update_product_quantity(product_id, new_quantity):
    """Обновляет количество блюда на кухне в таблице 'Товар'."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE Товар SET количество = ? WHERE id = ?", (new_quantity, product_id))
    conn.commit()
    conn.close()

def get_product_quantity(product_id):
    """Возвращает текущий остаток порций блюда по его id."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT количество FROM Товар WHERE id = ?", (product_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0
