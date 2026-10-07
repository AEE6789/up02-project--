"""Форма просмотра товара проекта Кулинария."""
import tkinter as tk
from tkinter import ttk, messagebox

from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_HEADER, FONT_SIZE_TITLE, font
)
from resources import get_product_image


class ViewForm:
    """Форма просмотра выбранного блюда кулинарии Варианта №20."""
    
    def __init__(self, parent, product, on_add_to_order=None):
        self.product = product
        self.on_add_to_order = on_add_to_order
        
        self.window = tk.Toplevel(parent)
        self.window.title(f"Просмотр — {product[2]}")  # Название на индексе 2
        self.window.geometry("700x600")
        self.window.configure(bg=COLOR_MAIN_BG)
        
        self.build_ui()
    
    def build_ui(self):
        """Строит интерфейс формы."""
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="КАРТОЧКА ТОВАРА",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)
        
        main = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        main.pack(fill="both", expand=True, padx=20, pady=20)
        
        img_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        img_frame.pack(side="left", padx=10)
        
        # Твой живой индекс фото из SQLite — 6
        photo = get_product_image(self.product[6], size=(200, 200))
        if photo:
            img_label = tk.Label(img_frame, image=photo, bg=COLOR_MAIN_BG)
            img_label.image = photo
            img_label.pack()
        else:
            tk.Label(img_frame, text="[НЕТ ФОТО]", bg=COLOR_MAIN_BG, width=15, height=8, relief="solid").pack()
        
        info_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        info_frame.pack(side="left", fill="both", expand=True, padx=20)
        
        # Вызовы полей под твою структуру СУБД (Задание 4.2)
        self._add_field(info_frame, "Наименование блюда", self.product[2])
        self._add_field(info_frame, "Категория", self.product[1])
        self._add_field(info_frame, "Состав рецептуры", self.product[3] if self.product[3] else "[Не указан]")
        self._add_field(info_frame, "Стоимость порции", f"{self.product[4]} руб.")
        self._add_field(info_frame, "Доступно на кухне", f"{self.product[5]} шт.")
        
        # Кнопки (Задание 4.3)
        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(fill="x", pady=10)
        
        btn_add = tk.Button(btn_frame, text="Добавить в заказ", command=self.add_to_order,
                            bg=COLOR_ACCENT, fg="white", font=font(FONT_SIZE_NORMAL, bold=True), padx=15, pady=5)
        btn_add.pack(side="left", padx=20)
        
        btn_back = tk.Button(btn_frame, text="Назад", command=self.window.destroy,
                             bg="gray", fg="white", font=font(FONT_SIZE_NORMAL), padx=15, pady=5)
        btn_back.pack(side="right", padx=20)
    
    def _add_field(self, parent, label, value):
        # Реализация Задания 4.1
        row = tk.Frame(parent, bg=COLOR_MAIN_BG)
        row.pack(fill="x", pady=4)
        
        label_txt = tk.Label(row, text=f"{label}:", font=font(FONT_SIZE_NORMAL, bold=True), 
                             width=18, anchor="w", bg=COLOR_MAIN_BG)
        label_txt.pack(side="left")
        
        value_txt = tk.Label(row, text=str(value), font=font(FONT_SIZE_NORMAL), 
                             anchor="w", bg=COLOR_MAIN_BG, justify="left", wraplength=450)
        value_txt.pack(side="left", fill="x", expand=True)
    
    def add_to_order(self):
        # Реализация Задания 4.4
        if not self.on_add_to_order:
            messagebox.showinfo("Информация", "Функция в разработке")
            return
        if not self.product:
            messagebox.showerror("Ошибка", "Товар не выбран")
            return
        try:
            self.on_add_to_order(self.product)
            messagebox.showinfo("Успех", "Товар добавлен в заказ")
        except Exception as e:
            messagebox.showerror("Ошибка заказа", f"Не удалось добавить товар:\n{e}")
