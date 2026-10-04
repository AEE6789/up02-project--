"""
Мой модуль для работы с медиа-ресурсами проекта «Кулинария».
"""
import os
from PIL import Image, ImageTk

# Пути к ресурсам
PATH_PICTURE = "resources/picture.png"
PATH_LOGO = "resources/logo.png"
PATH_ICON = "resources/icon.ico"

def load_image(path, size=(100, 100)):
    """Загружаю картинку с жесткой обрезкой под размер (для сетки товаров)."""
    try:
        if not os.path.exists(path):
            return None
        img = Image.open(path).resize(size)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Ошибка загрузки {path}: {e}")
        return None

def load_image_proportional(path, max_size=(100, 100)):
    """Загружаю логотип с сохранением пропорций, чтобы бренд не поплыл."""
    try:
        if not os.path.exists(path):
            return None
        img = Image.open(path)
        img.thumbnail(max_size)   # сохраняет пропорции!
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Ошибка загрузки {path}: {e}")
        return None

def get_product_image(image_path, size=(100, 100)):
    """Автоматически подставляю picture.png, если у товара нет своего фото."""
    full_path = f"resources/{image_path}" if image_path else PATH_PICTURE
    if not image_path or not os.path.exists(full_path):
        return load_image(PATH_PICTURE, size)
    return load_image(full_path, size)
