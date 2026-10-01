"""Расширенное тестирование алгоритма скидки (5 новых тест-кейсов)."""
from datetime import datetime
from discount import calculate_price_with_discount


def run_extended_tests():
    print("=" * 80)
    print("РАСШИРЕННОЕ ТЕСТИРОВАНИЕ АЛГОРИТМА СКИДКИ (ДОМАШНЕЕ ЗАДАНИЕ)")
    print("=" * 80)

    # Список тестов: (id, базовая_цена, дата_расчета, ожидание, пояснение)
    test_cases = [
        # (id, базовая_цена, дата_расчета, ожидание, пояснение)
        (4, 450, datetime(2026, 10, 15), 337.5, "Медовик (15.10): прошлый месяц сентябрь, заказов нет -> Скидка 25%"),
        (1, 300, datetime(2026, 11, 20), 225.0, "Щи (20.11): прошлый месяц октябрь, в октябре заказов 0 -> Скидка 25%"),
        (2, 400, datetime(2026, 11, 1), 300.0, "Котлеты (01.11): прошлый месяц октябрь, в октябре заказов 0 -> Скидка 25%"),
        (5, 100, datetime(2026, 12, 10), 75.0, "Морс (10.12): прошлый месяц ноябрь, в ноябре заказов 0 -> Скидка 25%"),
        (7, 380, datetime(2026, 10, 25), 285.0, "Цезарь (25.10): прошлый месяц сентябрь, заказов нет -> Скидка 25%"),
    ]


    passed = 0
    for product_id, price, date, expected, comment in test_cases:
        result = calculate_price_with_discount(product_id, price, date)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(f"{status} Блюдо {product_id} на дату {date.strftime('%d.%m.%Y')}: "
              f"{price} руб. → {result} руб. (ожидалось {expected})")
        print(f"   💡 {comment}\n")

    print("=" * 80)
    print(f"Успешно пройдено расширенных тестов: {passed} / {len(test_cases)}")
    print("=" * 80)


if __name__ == "__main__":
    run_extended_tests()
