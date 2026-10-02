"""Домашнее задание: Полное тестирование граничных случаев алгоритма скидки."""
from datetime import datetime
from discount import calculate_price_with_discount

def print_test_report(passed, total):
    """Выводит отчет по Заданию 2 ДЗ."""
    print("\n" + "=" * 40)
    print("ОТЧЁТ О ТЕСТИРОВАНИИ")
    print(f"Пройдено: {passed} / {total}")
    if passed == total:
        print("Результат: ✅ УСПЕХ")
    else:
        print("Результат: ❌ ЕСТЬ ОШИБКИ")
    print("=" * 40)

def run_homework_tests():
    # 5 Новых тестов на граничные случаи (Задание 1)
    test_cases = [
        # (product_id, price, date, expected, comment)
        (1, 300, datetime(2026, 10, 1), 300.0, "Граничный случай: 1-е число месяца (октябрь)"),
        (1, 300, datetime(2026, 10, 31), 300.0, "Граничный случай: Последний день месяца (октябрь)"),
        (4, 0, datetime(2026, 10, 15), 0.0, "Граничный случай: Товар с нулевой ценой"),
        (4, 450, datetime(2026, 12, 15), 337.5, "Товар с продажами в позапрошлом месяце (сентябре), но не в предыдущем (ноябре)"),
        (5, 100, datetime(2026, 10, 15), 75.0, "Обычный товар без заказов в原始 сентябре"),
    ]

    print("=" * 75)
    print("ДОМАШНЕЕ ЗАДАНИЕ: ТЕСТИРОВАНИЕ ГРАНИЧНЫХ СЛУЧАЕВ")
    print("=" * 75)

    passed = 0
    for product_id, price, date, expected, comment in test_cases:
        result = calculate_price_with_discount(product_id, price, date)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(f"{status} Код {product_id} на {date.date()}: {price} руб. → {result} руб. — {comment}")

    print_test_report(passed, len(test_cases))

if __name__ == "__main__":
    run_homework_tests()
