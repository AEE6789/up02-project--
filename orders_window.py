"""Окно списка заказов для Менеджера кулинарии Варианта №20."""
import tkinter as tk
from tkinter import ttk, messagebox
from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_HEADER, FONT_SIZE_TITLE, font
)
import order_manager as om


class OrdersWindow:
    """Окно списка заказов."""

    def __init__(self, parent, current_user=None):
        """
        Инициализация окна с контролем ролей.
        :param parent: родительское окно
        :param current_user: кортеж текущего авторизованного пользователя
        """
        self.current_user = current_user
        self.window = tk.Toplevel(parent)
        self.window.title("Список заказов")
        self.window.geometry("800x500")
        self.window.configure(bg=COLOR_MAIN_BG)

        self.build_ui()
        self.load_orders()

    def build_ui(self):
        """Строит интерфейс окна журнала."""
        # Шапка окна
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="СПИСОК ЗАКАЗОВ КУЛИНАРИИ",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)

        # Таблица заказов на базе ttk.Treeview
        columns = ("id", "date", "client")
        self.tree = ttk.Treeview(self.window, columns=columns,
                                 show="headings", height=15)

        self.tree.heading("id", text="№ Заказа")
        self.tree.heading("date", text="Дата оформления")
        self.tree.heading("client", text="ФИО Заказчика")

        self.tree.column("id", width=80, anchor="center")
        self.tree.column("date", width=150, anchor="center")
        self.tree.column("client", width=500, anchor="w")

        self.tree.pack(fill="both", expand=True, padx=20, pady=20)

        # Привязка двойного щелчка ЛКМ для перехода к составу
        self.tree.bind("<Double-1>", self.on_order_select)

        # Контейнер кнопок управления
        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(fill="x", pady=10)

        tk.Button(btn_frame, text="Просмотр состава (ЛКМ x2)",
                  command=self.on_order_select,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(side="left", padx=20)

        tk.Button(btn_frame, text="Обновить журнал",
                  command=self.load_orders,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(side="left", padx=10)

        tk.Button(btn_frame, text="Назад в каталог",
                  command=self.window.destroy,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(side="right", padx=20)

    def load_orders(self):
        """Загружает заголовки заказов из БД."""
        # Очищаем сетку таблицы перед вычиткой
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            orders = om.get_all_orders()
            for order in orders:
                self.tree.insert("", tk.END, values=order)
        except Exception as e:
            messagebox.showerror("Ошибка СУБД", f"Не удалось загрузить заказы:\n{e}")

    def on_order_select(self, event=None):
        """Обработчик выбора заказа."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Пожалуйста, выделите строку из журнала.")
            return

        item = self.tree.item(selected[0])
        order_id = item["values"][0]

        # Открываем окно состава заказа (Пара 25)
        from order_items_window import OrderItemsWindow
        OrderItemsWindow(self.window, order_id)
