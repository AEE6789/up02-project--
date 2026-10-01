"""Загрузка заказов из БД в объекты класса Order (ДЗ: Задание 3)."""
import sqlite3
from config import DB_PATH
from models import Product, Order


def get_all_orders():
    """Возвращает список объектов Order, связанных с объектами Product."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # SQL-запрос связывает Заказ и Товар.
    query = """
        SELECT 
            З.id, З.дата, З.клиент, З.количество,
            Т.id, Т.категория, Т.название, Т.состав, Т.цена, Т.количество, Т.фото
        FROM Заказ З
        JOIN Товар Т ON З.товар_id = Т.id
        ORDER BY З.дата DESC
    """
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()

    orders = []
    for row in rows:
        # Собираем объект Product из данных таблицы Товар (индексы с 4 по 10)
        product = Product(
            product_id=row[4],
            category=row[5],
            name=row[6],
            composition=row[7],
            price=row[8],
            quantity=row[9],
            photo=row[10]
        )
        
        # Собираем объект Order, передавая внутрь объект product
        order = Order(
            order_id=row[0],
            date=row[1],
            client=row[2],
            product=product,
            quantity=row[3]
        )
        orders.append(order)
        
    return orders


def print_orders_report(orders):
    """Выводит подробный отчет по заказам."""
    print(f"\n{'=' * 85}")
    print(f"ОТЧЕТ ПО ЗАКАЗАМ ({len(orders)} шт.)")
    print("=" * 85)
    
    grand_total = 0
    for o in orders:
        print(o.info())
        grand_total += o.total()
        
    print("=" * 85)
    print(f"ИТОГО ПО ВСЕМ ЗАКАЗАМ: {grand_total} руб.")
    print("=" * 85)


if __name__ == "__main__":
    try:
        orders = get_all_orders()
        print_orders_report(orders)
    except sqlite3.OperationalError as e:
        print(f"Ошибка БД! Проверьте названия таблиц и полей: {e}")
