"""Тестирование подсветки товаров кулинарии."""
from catalog import _get_card_color
from styles import COLOR_HIGHLIGHT, COLOR_MAIN_BG


def test_highlight():
    """Прогон тестов для подсветки с учетом порога 12 штук."""
    test_cases = [
        # (qty, expected_color, comment)
        (20, COLOR_MAIN_BG, "20 > 12 — нет подсветки"),
        (15, COLOR_MAIN_BG, "15 > 12 — нет подсветки"),
        (12, COLOR_HIGHLIGHT, "12 ≤ 12 — подсветка (граница)"),
        (5, COLOR_HIGHLIGHT, "8 ≤ 12 — подсветка"),
        (25, COLOR_MAIN_BG, "25 > 12 — нет подсветки"),
        (10, COLOR_HIGHLIGHT, "10 ≤ 12 — подсветка"),
        (14, COLOR_MAIN_BG, "14 > 12 — нет подсветки"),
    ]

    print("=" * 70)
    print("ТЕСТИРОВАНИЕ ПОДСВЕТКИ (ПОРОГ 12)")
    print("=" * 70)

    passed = 0
    for qty, expected, comment in test_cases:
        result = _get_card_color(qty)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(f"{status} qty={qty}: {result} "
              f"(ожидалось {expected}) — {comment}")

    print("=" * 70)
    print(f"Пройдено: {passed} / {len(test_cases)}")


if __name__ == "__main__":
    test_highlight()


# Дополнительные тесты бизнес-логики ДЗ
assert _get_card_color(1000) == "white", "Ошибка: Большое число 1000 не должно подсвечиваться"
assert _get_card_color(-1) == "#ff8080", "Ошибка: Отрицательное значение -1 должно вызывать аварийный цвет"
assert _get_card_color(12) == "#ff8080", "Ошибка: Пограничное значение 3 должно стабильно подсвечиваться"
