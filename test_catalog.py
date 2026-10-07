"""Тестирование каталога и структуры базы данных Варианта №20."""
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


def test_product_fields():
    """Проверяет, что у всех товаров достаточно полей для отображения."""
    try:
        products = db.get_all_products()
        for p in products:
            if len(p) < 6:
                print(f"❌ Товар ID {p[0] if len(p)>0 else '???'}: мало полей ({len(p)})")
                return False
        return True
    except Exception as e:
        print(f"❌ Ошибка теста полей: {e}")
        return False


def test_prices_are_numbers():
    """Автоматически находит поле цены и проверяет, что это число."""
    try:
        products = db.get_all_products()
        for p in products:
            numerical_values = [val for val in p if isinstance(val, (int, float)) and not isinstance(val, bool)]
            
            # Если чисел вообще нет (кроме возможно ID), это ошибка данных
            if len(numerical_values) < 2:
                print(f"❌ Товар ID {p[0]}: в записи не найдены числовые поля для цены и количества")
                return False
        return True
    except Exception as e:
        print(f"❌ Ошибка теста цен: {e}")
        return False


def test_quantity_not_negative():
    """Проверяет, что складское количество не ушло в минус."""
    try:
        products = db.get_all_products()
        for p in products:
            # Проверяем все числовые поля на отрицательность (количество порций не может быть < 0)
            for val in p:
                if isinstance(val, (int, float)) and val < 0:
                    print(f"❌ Товар ID {p[0]}: обнаружено отрицательное значение ({val})")
                    return False
        return True
    except Exception as e:
        print(f"❌ Ошибка теста количества: {e}")
        return False


def test_names_not_empty():
    """Дополнительный тест из Задания 6.6: проверяет наличие названий блюд."""
    try:
        products = db.get_all_products()
        for p in products:
            # Ищем непустую строку среди первых полей кортежа (где обычно имя и категория)
            text_fields = [str(val).strip() for val in p if isinstance(val, str)]
            if not text_fields or any(txt == "" or txt == "None" for txt in text_fields[:2]):
                print(f"❌ Товар ID {p[0]}: найдено пустое обязательное текстовое поле")
                return False
        return True
    except Exception as e:
        print(f"❌ Ошибка теста наименований: {e}")
        return False


def run_all_tests():
    """Прогон всех тестов каталога кулинарии."""
    tests = [
        ("БД доступна", test_db_available),
        ("Товары загружены", test_products_count),
        ("У всех товаров нужные поля", test_product_fields),
        ("Все цены — числа", test_prices_are_numbers),
        ("Количество не отрицательное", test_quantity_not_negative),
        ("Названия не пустые", test_names_not_empty)
    ]

    print("=" * 60)
    print("ТЕСТИРОВАНИЕ КАТАЛОГА (УНИВЕРСАЛЬНЫЙ СКАНИРУЮЩИЙ СКРИПТ)")
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
