"""Тестирование алгоритма скидки для кулинарии (включая новые тесты)."""
from datetime import datetime
from discount import calculate_price_with_discount

def run_tests():
    test_cases = [
        # Из КИМ ДЭ на дату 15.10.2026 (прошлый месяц - сентябрь)
        (1, 300, datetime(2026, 10, 15), 300.0, "Щи — заказы в сентябре были -> Скидки нет"),
        (2, 400, datetime(2026, 10, 15), 400.0, "Котлеты — заказы в сентябре были -> Скидки нет"),
        (3, 350, datetime(2026, 10, 15), 350.0, "Мимоза — заказы в сентябре были -> Скидки нет"),
        (4, 450, datetime(2026, 10, 15), 337.5, "Медовик — заказов in сентябре нет -> Скидка 25%"),
        (5, 100, datetime(2026, 10, 15), 75.0, "Морс — заказов в сентябре нет -> Скидка 25%"),
        
        # Дополнительные тесты (Задание 4.2)
        (2, 400, datetime(2026, 11, 15), 300.0, "Котлеты в ноябре: в октябре заказов не было -> Скидка 25%"),
        (1, 300, datetime(2026, 11, 15), 225.0, "Щи в ноябре: в октябре заказов не было -> Скидка 25%"),
        (4, 450, datetime(2026, 9, 1), 337.5, "Медовик (01.09): в августе заказов не было -> Скидка 25%"),
    ]

    print("=" * 80)
    print("РАСШИРЕННОЕ ТЕСТИРОВАНИЕ АЛГОРИТМА СКИДКИ")
    print("=" * 80)

    passed = 0
    for product_id, price, date, expected, comment in test_cases:
        result = calculate_price_with_discount(product_id, price, date)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(f"{status} Блюдо {product_id} на {date.date()}: "
              f"{price} → {result} (ожидалось {expected}) — {comment}")

    print("=" * 80)
    print(f"Пройдено успешно: {passed} / {len(test_cases)}")

if __name__ == "__main__":
    run_tests()
