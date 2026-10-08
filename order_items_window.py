"""Окно состава заказа проекта Кулинария."""
import tkinter as tk
from tkinter import ttk, messagebox
from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_TITLE, font
)
import order_manager as om


class OrderItemsWindow:
    """Окно состава заказа."""

    def __init__(self, parent, order_id):
        """
        Инициализация окна.
        :param parent: родительское окно
        :param order_id: id заказа
        """
        self.order_id = order_id
        self.window = tk.Toplevel(parent)
        self.window.title(f"Состав заказа №{order_id}")
        self.window.geometry("850x500")
        self.window.configure(bg=COLOR_MAIN_BG)

        self.build_ui()
        self.load_items()

    def build_ui(self):
        """Строит интерфейс окна."""
        # Шапка
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text=f"СОСТАВ ЗАКАЗА №{self.order_id}",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)

        # Таблица позиций (6 колонок под структуру Варианта №20)
        columns = ("name", "category", "size",
                   "quantity", "price", "total")
        self.tree = ttk.Treeview(self.window, columns=columns,
                                 show="headings", height=12)

        self.tree.heading("name", text="Наименование блюда")
        self.tree.heading("category", text="Категория")
        self.tree.heading("size", text="Размер порции")
        self.tree.heading("quantity", text="Кол-во")
        self.tree.heading("price", text="Цена")
        self.tree.heading("total", text="Сумма")

        self.tree.column("name", width=220, anchor="w")
        self.tree.column("category", width=120, anchor="w")
        self.tree.column("size", width=110, anchor="center")
        self.tree.column("quantity", width=70, anchor="center")
        self.tree.column("price", width=100, anchor="e")
        self.tree.column("total", width=100, anchor="e")

        self.tree.pack(fill="both", expand=True, padx=20, pady=20)

        # Итоговая сумма чека
        self.total_label = tk.Label(self.window, text="",
                                    font=font(FONT_SIZE_NORMAL, bold=True),
                                    fg=COLOR_ACCENT, bg=COLOR_MAIN_BG)
        self.total_label.pack(pady=10)

        # Кнопки управления
        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(fill="x", pady=10)

        tk.Button(btn_frame, text="Обновить данные",
                  command=self.load_items,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(side="left", padx=20)

        tk.Button(btn_frame, text="Назад к журналу",
                  command=self.window.destroy,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(side="right", padx=20)

    def load_items(self):
        """Загружает позиции заказа из БД через JOIN."""
        # Очищаем таблицу перед выводом
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            items = om.get_order_items(self.order_id)
            if not items:
                messagebox.showinfo("Информация", "Заказ пуст")
                return

            for item in items:
                # Структура: (id, название, категория, размер, количество, цена)
                name = item[1]
                category = item[2]
                size = item[3]
                quantity = item[4]
                price = item[5]
                item_total = quantity * price

                self.tree.insert("", tk.END,
                                 values=(name, category, size,
                                         quantity,
                                         f"{price:.2f}",
                                         f"{item_total:.2f}"))

            # Вывод агрегированной итоговой суммы чека
            total = om.get_order_total(self.order_id)
            self.total_label.config(
                text=f"ИТОГО ПО ЧЕКУ ЗАКАЗА: {total:.2f} руб."
            )
        except Exception as e:
            messagebox.showerror("Ошибка СУБД", f"Не удалось загрузить состав:\n{e}")
