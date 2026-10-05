"""
Каталог товаров проекта «Кулинария».

"""
import tkinter as tk
from tkinter import ttk

# Импорт цветов и шрифтов (Задание 7.4)
from styles import (
    COLOR_HIGHLIGHT, FONT_SIZE_NORMAL, FONT_SIZE_HEADER, font
)
# Импорт умного загрузчика картинок (Задание 4.4)
from resources import get_product_image

def create_product_card(parent, product):
    qty = product[5] if product[5] is not None else 0
    bg_color = COLOR_HIGHLIGHT if qty <= 12 else "white"

    card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=5)

    # === Изображение (слева) ===
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)

    # Загрузка через модуль ресурсов (Задание 4.4)
    photo = get_product_image(product[6], size=(100, 100))
    
    if photo:
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.image = photo   
        img_label.pack()
    else:
        tk.Label(img_frame, text="[НЕТ ФОТО]", bg=bg_color, font=font(), width=10, height=5).pack()

    # === Текстовая часть (справа) ===
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # === ЗАДАНИЕ 5.4 и ДЗ 2: Проверка значений на крайние случаи ===
    raw_name = str(product[2]) if product[2] else "[Без названия]"
    # ДЗ 2: Если название блюда > 100 символов, аккуратно обрезаем его
    name = raw_name[:97] + "..." if len(raw_name) > 100 else raw_name

    category = str(product[1]) if product[1] else "[Без категории]"
    composition = str(product[3]) if product[3] else "[Состав не указан]"
    
    raw_price = product[4] if product[4] is not None else 0
    # ДЗ 2: Если цена больше 1 000 000 руб, пишем заглушку
    price_text = "Цена по запросу" if raw_price > 1000000 else f"{raw_price} руб."

    # Применение централизованного шрифта (Задание 7.5)
    title = f"Кулинария | {name}"
    tk.Label(text_frame, text=title, font=font(FONT_SIZE_HEADER, bold=True), bg=bg_color, anchor="w").pack(fill="x")

    tk.Label(text_frame, text=f"Категория: {category}", font=font(FONT_SIZE_NORMAL), fg="#555555", bg=bg_color, anchor="w").pack(fill="x")

    row_middle = tk.Frame(text_frame, bg=bg_color)
    row_middle.pack(fill="x", pady=2)

    # Вызов индикатора по ТЗ Пары 13 (порог 5 штук)
    indicator = _indicator(qty)
    qty_text = f"Количество: {indicator} ({qty} шт.)"
    tk.Label(row_middle, text=qty_text, font=font(FONT_SIZE_NORMAL), bg=bg_color, anchor="w").pack(side="left")

    # Вывод цены с учетом проверки ДЗ 2
    tk.Label(row_middle, text=price_text, font=font(FONT_SIZE_HEADER, bold=True), fg="darkgreen", bg=bg_color, anchor="e").pack(side="right")

    comp_text = f"Состав: {composition}"
    tk.Label(text_frame, text=comp_text, font=font(FONT_SIZE_NORMAL), fg="#444444", bg=bg_color, anchor="w", justify="left", wraplength=430).pack(fill="x", pady=(5, 0))

    # Линия-разделитель снизу (Домашнее задание 1)
    separator = tk.Frame(parent, height=2, bg="#70B2AF")
    separator.pack(fill="x", padx=10, pady=4)
    
    return card

# Вспомогательная функция отчета (также защищена ДЗ 2)
def _add_text_info(card, product, bg_color, qty):	
    """Добавляет текстовую информацию о товаре кулинарии."""
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    raw_name = str(product[2]) if product[2] else "[Без названия]"
    name = raw_name[:97] + "..." if len(raw_name) > 100 else raw_name
    category = str(product[1]) if product[1] else "[Без категории]"
    composition = str(product[3]) if product[3] else "[Состав не указан]"
    
    raw_price = product[4] if product[4] is not None else 0
    price_text = "Цена по запросу" if raw_price > 1000000 else f"{raw_price} руб."

    _add_label(text_frame, f"Кулинария | {name}", bg_color, bold=True, size=FONT_SIZE_HEADER)
    _add_label(text_frame, f"Категория: {category}", bg_color)
    
    row_middle = tk.Frame(text_frame, bg=bg_color)
    row_middle.pack(fill="x", pady=2)
    _add_label(row_middle, f"Количество: {_indicator(qty)} ({qty} шт.)", bg_color, side="left")
    _add_label(row_middle, price_text, bg_color, bold=True, size=FONT_SIZE_HEADER, align="e", side="right", fg="darkgreen")
    
    _add_label(text_frame, f"Состав: {composition}", bg_color)

def _add_label(parent, text, bg_color, bold=False, size=FONT_SIZE_NORMAL, align="w", side=None, fg="black"):
    """Вспомогательный метод для отображения меток с поддержкой позиционирования."""
    lbl = tk.Label(parent, text=text, font=font(size, bold=bold), bg=bg_color, anchor=align, fg=fg)
    if side:
        lbl.pack(side=side)
    else:
        lbl.pack(fill="x")

def _indicator(qty):
    """Индикатор «много/мало» по спецификации КИМ (порог 5 штук)."""
    return "много" if qty > 12 else "мало"
