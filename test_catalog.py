"""Тестирование каталога на основе реальной структуры базы данных (7 полей)."""
import database as db



def test_db_available():
    """Проверяет, что БД доступна."""
    try:
        products = db.get_all_products()
        return isinstance(products, list)
    except Exception as e:
        print(f"❌ БД недоступна: {e}")
        return False


def test_products_count():
    """Проверяет, что товары загружены."""
    try:
        products = db.get_all_products()
        return len(products) > 0
    except Exception:
        return False


def test_product_fields_count():
    """Проверяет, что у всех товаров ровно 7 полей согласно скриншоту."""
    try:
        products = db.get_all_products()
        for p in products:
            if len(p) != 7:
                print(f"❌ Товар id={p[0]}: неверное количество полей ({len(p)} вместо 7)")
                return False
        return True
    except Exception:
        return False


def test_prices_are_numbers():
    """Проверяет, что все цены (индекс 4) — числа."""
    try:
        products = db.get_all_products()
        for p in products:
            if not isinstance(p[4], (int, float)):
                print(f"❌ Товар id={p[0]}: цена на индексе 4 не число")
                return False
        return True
    except Exception:
        return False


def test_quantity_not_negative():
    """Проверяет, что количество (индекс 5) не отрицательное."""
    try:
        products = db.get_all_products()
        for p in products:
            if p[5] < 0:
                print(f"❌ Товар id={p[0]}: отрицательное количество")
                return False
        return True
    except Exception:
        return False


def test_at_least_one_image():
    """
    Выполнение Домашнего задания №2.
    Проверяет, что хотя бы у одного товара есть изображение на твоём индексе 6.
    """
    try:
        products = db.get_all_products()
        for p in products:
            # Твой реальный индекс 6 (поле фото: shi.png, kotlety.png и т.д.)
            photo_field = p[6]
            if photo_field is not None and str(photo_field).strip() != "" and str(photo_field) != "None":
                return True  # Файл картинки найден, тест пройден успешно!
        
        print("❌ Ошибка ДЗ: ни у одного товара в БД нет изображения")
        return False
    except Exception as e:
        print(f"❌ Сбой при проверке картинок: {e}")
        return False


def run_all_tests():
    """Прогон всех тестов каталога кулинарии."""
    tests = [
        ("БД доступна для подключения", test_db_available),
        ("Товары успешно загружены из таблиц", test_products_count),
        ("У всех товаров ровно 7 полей в строке", test_product_fields_count),
        ("Все цены на индексе 4 — числа", test_prices_are_numbers),
        ("Количество на индексе 5 не отрицательное", test_quantity_not_negative),
        ("Хотя бы у одного товара есть фото (ДЗ 2, индекс 6)", test_at_least_one_image),
    ]

    print("=" * 60)
    print("ТЕСТИРОВАНИЕ КАТАЛОГА (СТРОГО ПО СКРИНШОТАМ БД)")
    print("=" * 60)

    passed = 0
    for name, func in tests:
        result = func()
        status = "✅" if result else "❌"
        if result:
            passed += 1
        print(f"{status} {name}")

    print("=" * 60)
    print(f"Пройдено: {passed} / {len(tests)}")


if __name__ == "__main__":
    run_all_tests()
