"""
Каталог товаров проекта «Кулинария».
Разработчик: mawr89-rgb
Дата: 04.10.2026
"""
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

# Подгружаем константы из config.py (если файла нет, используются значения по умолчанию)
try:
    from config import DB_PATH, COLOR_HIGHLIGHT, FONT_FAMILY
except ImportError:
    COLOR_HIGHLIGHT = "#ff8080"
    FONT_FAMILY = "Arial"

def create_product_card(parent, product):
    """
    Создаёт карточку товара строго по макету и схеме на основе кортежа вашей БД.
    Порядок полей в вашей таблице «Товар»:
    0: id, 1: категория, 2: название, 3: состав, 4: цена, 5: количество, 6: фото
    """
    qty = product[5]   # Индекс столбца 'количество' в вашей БД
    bg_color = COLOR_HIGHLIGHT if qty <= 12 else "white"

    # Контейнер карточки с рамкой
    card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=5)

    # === Изображение (слева) ===
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)

    # Индекс 6 — имя файла картинки в вашей БД
    image_name = product[6]
    image_path = f"resources/{image_name}" if image_name else "resources/picture.png"
    if not os.path.exists(image_path):
        image_path = "resources/picture.png"

    try:
        img = Image.open(image_path).resize((100, 100))
        photo = ImageTk.PhotoImage(img)
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.image = photo   # Жесткая ссылка от сборщика мусора
        img_label.pack()
    except Exception:
        tk.Label(img_frame, text="[ФОТО]", bg=bg_color, width=12, height=5, relief="sunken").pack()

    # === Текстовая содержательная часть (справа от фото) ===
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # 1. Производство | Наименование (Индекс 2 — название)
    title = f"Кулинария | {product[2]}"
    tk.Label(text_frame, text=title, font=(FONT_FAMILY, 13, "bold"), bg=bg_color, anchor="w").pack(fill="x")

    # 2. Категория под названием (Индекс 1 — категория)
    tk.Label(text_frame, text=f"Категория: {product[1]}", font=(FONT_FAMILY, 10), fg="#555555", bg=bg_color, anchor="w").pack(fill="x")

    # 3. Строка-строчка: Количество СЛЕВА + Цена СПРАВА (На одной линии)
    row_middle = tk.Frame(text_frame, bg=bg_color)
    row_middle.pack(fill="x", pady=2)

    # Индикатор количества
    indicator = "много" if qty >= 12 else "мало"
    qty_text = f"Количество: {indicator} ({qty} шт.)"
    tk.Label(row_middle, text=qty_text, font=(FONT_FAMILY, 11), bg=bg_color, anchor="w").pack(side="left")

    # Цена (Прижата к правому краю, индекс 4 — цена)
    price_text = f"{product[4]} руб."
    tk.Label(row_middle, text=price_text, font=(FONT_FAMILY, 13, "bold"), fg="darkgreen", bg=bg_color, anchor="e").pack(side="right")

    # 4. Состав (В самом низу карточки, индекс 3 — состав)
    comp_text = f"Состав: {product[3]}"
    tk.Label(text_frame, text=comp_text, font=(FONT_FAMILY, 9, "italic"), fg="#444444", bg=bg_color, anchor="w", justify="left", wraplength=430).pack(fill="x", pady=(5, 0))

    return card
