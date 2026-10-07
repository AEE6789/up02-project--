"""Тестирование подсветки."""
from catalog import _get_card_color
from styles import COLOR_HIGHLIGHT, COLOR_MAIN_BG


def test_color():
    """Прогон тестов для подсветки с учетом индивидуального порога 12."""
    test_cases = [
        (20, COLOR_MAIN_BG, "20 > 12 — без подсветки"),
        (13, COLOR_MAIN_BG, "13 > 12 — граница нормы (без подсветки)"),
        (12, COLOR_HIGHLIGHT, "12 <= 12 — точная граница (подсветка КИМ!)"),
        (8, COLOR_HIGHLIGHT, "8 <= 12 — меньше 12 (подсветка)"),
        (3, COLOR_HIGHLIGHT, "3 <= 12 — минимальный остаток"),
        (0, COLOR_HIGHLIGHT, "0 <= 12 — нулевой остаток (подсветка)"),
                # 2 теста по заданию
        (100, COLOR_MAIN_BG, "большое число (100 > 12)"),
        (-1, COLOR_HIGHLIGHT, "отрицательное (крайний случай, -1 <= 12)"),

    ]

    print("=" * 60)
    print("ТЕСТИРОВАНИЕ ПОДСВЕТКИ (ПОРОГ 12)")
    print("=" * 60)

    passed = 0
    for qty, expected, comment in test_cases:
        result = _get_card_color(qty)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(f"{status} qty={qty}: {result} (ожидалось {expected}) — {comment}")

    print("=" * 60)
    print(f"Пройдено: {passed} / {len(test_cases)}")


if __name__ == "__main__":
    test_color()
