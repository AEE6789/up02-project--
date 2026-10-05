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

    # === ЗАДАНИЕ 5.4: Проверка значений на крайние случаи (тернарные операторы под Вариант 20) ===
    name = product[2] if product[2] else "[Без названия]"
    category = product[1] if product[1] else "[Без категории]"
    composition = product[3] if product[3] else "[Состав не указан]"
    price = product[4] if product[4] is not None else 0

    # Применение централизованного шрифта (Задание 7.5)
    title = f"Кулинария | {name}"
    tk.Label(text_frame, text=title, font=font(FONT_SIZE_HEADER, bold=True), bg=bg_color, anchor="w").pack(fill="x")

    tk.Label(text_frame, text=f"Категория: {category}", font=font(FONT_SIZE_NORMAL), fg="#555555", bg=bg_color, anchor="w").pack(fill="x")

    row_middle = tk.Frame(text_frame, bg=bg_color)
    row_middle.pack(fill="x", pady=2)

    indicator = "много" if qty >= 12 else "мало"
    qty_text = f"Количество: {indicator} ({qty} шт.)"
    tk.Label(row_middle, text=qty_text, font=font(FONT_SIZE_NORMAL), bg=bg_color, anchor="w").pack(side="left")

    price_text = f"{price} руб."
    tk.Label(row_middle, text=price_text, font=font(FONT_SIZE_HEADER, bold=True), fg="darkgreen", bg=bg_color, anchor="e").pack(side="right")

    comp_text = f"Состав: {composition}"
    tk.Label(text_frame, text=comp_text, font=font(FONT_SIZE_NORMAL), fg="#444444", bg=bg_color, anchor="w", justify="left", wraplength=430).pack(fill="x", pady=(5, 0))

    # Линия-разделитель снизу (Домашнее задание 1)
    separator = tk.Frame(parent, height=2, bg="#70B2AF")
    separator.pack(fill="x", padx=10, pady=4)
    
    return card

# Функция ниже добавлена в файл, так как она требуется бланком Задания 5.4 для отчета
def _add_text_info(card, product, bg_color, qty):	
    """Добавляет текстовую информацию о товаре кулинарии."""
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # Проверка значений (крайние случаи для Варианта №20 — Кулинария)
    name = product[2] if product[2] else "[Без названия]"
    category = product[1] if product[1] else "[Без категории]"
    composition = product[3] if product[3] else "[Состав не указан]"
    price = product[4] if product[4] is not None else 0

    # Вывод информации строго по макету КИМ
    _add_label(text_frame, f"Кулинария | {name}",
               bg_color, bold=True, size=FONT_SIZE_HEADER)
    _add_label(text_frame, f"Категория: {category}", bg_color)
    _add_label(text_frame, f"Количество: {_indicator(qty)} ({qty} шт.)", bg_color)
    _add_label(text_frame, f"Состав: {composition}", bg_color)
    _add_label(text_frame, f"{price} руб.",
               bg_color, bold=True, size=FONT_SIZE_HEADER, align="e")

def _add_label(parent, text, bg_color, bold=False, size=FONT_SIZE_NORMAL, align="w"):
    """Вспомогательный метод для отображения меток."""
    tk.Label(parent, text=text, font=font(size, bold=bold), bg=bg_color, anchor=align).pack(fill="x")

def _indicator(qty):
    """Определение остатка."""
    return "много" if qty >= 12 else "мало"
