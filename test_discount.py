"""Тестирование алгоритма скидки на основе реальной БД Кулинарии."""
from datetime import datetime
from discount import calculate_price_with_discount


def run_tests():
    """Прогон тестов по позициям из вашей БД."""
    date = datetime(2026, 10, 15)

    # (id, базовая цена из вашей БД, ожидаемая цена, пояснение)
    test_cases = [
        (1, 300, 300.0, "Щи — есть заказы в сентябре -> Скидки нет"),
        (2, 400, 400.0, "Котлеты — есть заказы в сентябре -> Скидки нет"),
        (3, 350, 350.0, "Мимоза — есть заказы в сентябре -> Скидки нет"),
        (4, 450, 337.5, "Медовик — нет заказов -> Скидка 25%"),
        (5, 100, 75.0, "Морс — нет заказов -> Скидка 25%"),
        (6, 480, 360.0, "Голубцы — нет заказов -> Скидка 25%"),
        (7, 380, 285.0, "Цезарь — нет заказов -> Скидка 25%"),
    ]

    print("=" * 75)
    print("ТЕСТИРОВАНИЕ АЛГОРИТМА СКИДКИ (БД: КУЛИНАРИЯ)")
    print("=" * 75)

    passed = 0
    for product_id, price, expected, comment in test_cases:
        result = calculate_price_with_discount(product_id, price, date)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(f"{status} Блюдо {product_id}: {price} руб. → {result} руб. "
              f"(ожидалось {expected}) — {comment}")

    print("=" * 75)
    print(f"Пройдено тестов: {passed} / {len(test_cases)}")


if __name__ == "__main__":
    run_tests()
