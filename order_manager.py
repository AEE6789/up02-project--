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


def create_order(client, items):
    """
    Создаёт заказ с несколькими позициями и пересчитывает остатки.
    :param client: ФИО клиента
    :param items: список кортежей (product_id, size, quantity, price)
    :return: id заказа или None
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        # 1. Создаём заголовок заказа (совместимость с NOT NULL и client на латинице)
        date = datetime.now().strftime("%Y-%m-%d")
        cur.execute(
            "INSERT INTO Заказ (дата, клиент, товар_id, количество) VALUES (?, ?, ?, ?)",
            (date, client, 0, 0)
        )
        order_id = cur.lastrowid

        # 2. Добавляем позиции И уменьшаем остатки еды на кухне кулинарии
        for product_id, size, quantity, price in items:
            # Проверяем наличие порций
            cur.execute("SELECT количество FROM Товар WHERE id = ?", (product_id,))
            row = cur.fetchone()
            if not row or row[0] < quantity:
                raise ValueError(f"Недостаточно товара id={product_id}")

            # Добавляем позицию в Состав_заказа
            cur.execute(
                "INSERT INTO Состав_заказа "
                "(заказ_id, товар_id, размер, количество, цена) "
                "VALUES (?, ?, ?, ?, ?)",
                (order_id, product_id, size, quantity, price)
            )

            # Автоматически уменьшаем остаток в таблице Товар
            cur.execute(
                "UPDATE Товар SET количество = количество - ? WHERE id = ?",
                (quantity, product_id)
            )

        # 3. Фиксируем ВСЁ, если все шаги цикла завершились успешно
        conn.commit()
        return order_id

    except Exception as e:
        conn.rollback()  # Полный откат изменений при любой ошибке
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

def decrease_product_quantity(product_id, quantity):
    """
    Уменьшает количество товара на складе (Пара 23, Задание 4.4).
    :param product_id: id товара
    :param quantity: на сколько уменьшить
    :return: True при успехе, False при ошибке
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        # Проверяем, что товара достаточно
        cur.execute("SELECT количество FROM Товар WHERE id = ?", (product_id,))
        row = cur.fetchone()
        if not row:
            return False

        current = row[0]
        if current < quantity:
            return False

        # Уменьшаем остаток порций блюда на кухне кулинарии
        cur.execute(
            "UPDATE Товар SET количество = количество - ? WHERE id = ?",
            (quantity, product_id)
        )
        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        print(f"Ошибка обновления: {e}")
        return False

    finally:
        conn.close()

def refresh_catalog(self):
    """Обновляет каталог."""
    # Удаляем все существующие карточки
    for widget in self.catalog_frame.winfo_children():
        widget.destroy()
    # Загружаем товары заново
    self.load_products()

