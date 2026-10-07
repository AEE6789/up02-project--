import tkinter as tk
from tkinter import ttk
import os

from styles import COLOR_SECONDARY_BG, COLOR_MAIN_BG, FONT_SIZE_TITLE, font
from config import APP_TITLE
import database as db
from catalog import create_product_card
from resources import load_image_proportional, PATH_LOGO, PATH_ICON

# Задание 6: безопасный вызов функций
from error_handler import safe_call


class CatalogWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry("900x700")
        self.root.configure(bg=COLOR_MAIN_BG)

        self.set_icon()
        self.build_ui()
        self.load_products()  # Первая загрузка 7 блюд

    def set_icon(self):
        """Установка иконки приложения."""
        try:
            if os.name == "nt":
                self.root.iconbitmap(PATH_ICON)
            else:
                icon_img = load_image_proportional(
                    PATH_ICON.replace(".ico", ".png"),
                    max_size=(32, 32)
                )
                if icon_img:
                    self.root.iconphoto(True, icon_img)
        except Exception as e:
            print(f"Не удалось установить иконку: {e}")

    def build_ui(self):
        """Отрисовка главного интерфейса каталога."""
        header = tk.Frame(self.root, bg=COLOR_SECONDARY_BG, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        logo = load_image_proportional(PATH_LOGO, max_size=(60, 60))
        if logo:
            logo_label = tk.Label(header, image=logo, bg=COLOR_SECONDARY_BG)
            logo_label.image = logo
            logo_label.pack(side="left", padx=15)
        else:
            tk.Label(header, text="[ЛОГОТИП]", font=font(),
                     bg="#70B2AF", fg="white", width=9, height=2).pack(side="left", padx=15)

        tk.Label(header, text="КАТАЛОГ ТОВАРОВ",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(expand=True)

        self.canvas = tk.Canvas(self.root, bg=COLOR_MAIN_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        
        self.catalog_frame = tk.Frame(self.canvas, bg=COLOR_MAIN_BG)
        self.catalog_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.catalog_frame, anchor="nw", width=870)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_products(self):
        """Безопасная загрузка ассортимента под контролем safe_call."""
        products = safe_call(db.get_all_products)
        if products is None:
            products = []
            
        for p in products:
            # Передача refresh-команды для реактивного обновления
            safe_call(create_product_card, self.catalog_frame, p, refresh=self.refresh_catalog)

    def refresh_catalog(self):
        """Очистка витрины и перерисовка карточек с новыми остатками."""
        for widget in self.catalog_frame.winfo_children():
            widget.destroy()
        self.load_products()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    CatalogWindow().run()
