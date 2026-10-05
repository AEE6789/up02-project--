"""Проверка вывода полей."""
import database as db


def test_fields():
    """Проверяет, что все поля на месте."""
    products = db.get_all_products()
    print(f"Всего товаров: {len(products)}")

    required_count = 6   # минимум полей для макета
    errors = 0
    has_image = False    # флаг для проверки наличия хотя бы одного фото

    for p in products:
        # 1. Ваша базовая проверка на количество полей
        if len(p) < required_count:
            print(f"❌ Товар id={p[0]}: мало полей ({len(p)})")
            errors += 1
            continue

        # 2. Проверка ДЗ: у всех товаров есть цена (индекс 4)
        if p[4] is None:
            print(f"❌ Товар id={p[0]}: нет цены")
            errors += 1

        # 3. Проверка ДЗ: у всех товаров количество >= 0 (индекс 5)
        if p[5] is not None and p[5] < 0:
            print(f"❌ Товар id={p[0]}: отрицательное количество ({p[5]})")
            errors += 1

        # 4. Проверка ДЗ: фиксация наличия изображения (индекс 6)
        if p[6] and str(p[6]).strip() != "":
            has_image = True

    # Проверка флага картинок после цикла
    if not has_image:
        print("❌ Ошибка: ни у одного товара нет изображения")
        errors += 1

    # Итоговый вывод результатов теста
    if errors == 0:
        print("✅ Все товары содержат нужные поля")
        print("✅ У всех товаров есть цена")
        print("✅ У всех товаров количество >= 0")
        print("✅ Хотя бы у одного товара есть изображение")
    else:
        print(f"❌ Найдено ошибок: {errors}")


if __name__ == "__main__":
    test_fields()
