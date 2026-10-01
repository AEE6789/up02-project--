"""Загрузка, фильтрация и вывод товаров из БД в объекты класса Product."""
import sqlite3
from config import DB_PATH
from models import Product


def get_all_products():
    """Возвращает список объектов Product из БД."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, категория, название, состав, цена, количество, фото FROM Товар ORDER BY id")
    rows = cur.fetchall()
    conn.close()

    products = []
    for row in rows:
        product = Product(
            product_id=row[0],
            category=row[1],
            name=row[2],
            composition=row[3],
            price=row[4],
            quantity=row[5],
            photo=row[6]
        )
        products.append(product)
    return products


def get_products_by_category(category):
    """Возвращает список объектов Product по конкретной категории."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, категория, название, состав, цена, количество, фото FROM Товар WHERE категория = ?", (category,))
    rows = cur.fetchall()
    conn.close()

    products = []
    for row in rows:
        product = Product(
            product_id=row[0],
            category=row[1],
            name=row[2],
            composition=row[3],
            price=row[4],
            quantity=row[5],
            photo=row[6]
        )
        products.append(product)
    return products


def get_products_low_stock():
    """Возвращает товары с критическим количеством (≤ 12)."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, категория, название, состав, цена, количество, фото FROM Товар WHERE количество <= 3")
    rows = cur.fetchall()
    conn.close()

    products = []
    for row in rows:
        product = Product(
            product_id=row[0],
            category=row[1],
            name=row[2],
            composition=row[3],
            price=row[4],
            quantity=row[5],
            photo=row[6]
        )
        products.append(product)
    return products


def print_catalog_with_highlight(products):
    """Выводит каталог с визуальной подсветкой (⚠️) для товаров с остатком ≤ 12."""
    print(f"\n{'=' * 70}")
    print(f"КАТАЛОГ ({len(products)} товаров)")
    print("=" * 70)

    for p in products:
        highlight = "⚠️" if p.quantity <= 12 else "  "
        print(f"{highlight} {p.info()}")

    print("=" * 70)


if __name__ == "__main__":
    print("1. ВСЕ ТОВАРЫ В МАГАЗИНЕ:")
    print_catalog_with_highlight(get_all_products())

    print("\n2. ТОВАРЫ КАТЕГОРИИ «Второе»:")
    # Подставьте вашу категорию, если в БД нет «Кроссовки»
    print_catalog_with_highlight(get_products_by_category("Второе"))

    print("\n3. ТОВАРЫ С НИЗКИМ ОСТАТКОМ (≤12):")
    print_catalog_with_highlight(get_products_low_stock())
