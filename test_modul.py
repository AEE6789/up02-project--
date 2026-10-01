from datetime import datetime
from models import Product

# Тест 1: Котлеты (id=2). Заказы в сентябре БЫЛИ -> цена не должна измениться
p1 = Product(2, "Второе", "Котлеты", "Мясо, хлеб, лук", 400, 15, "kotlety.png")
date = datetime(2026, 10, 15)
print(f"Блюдо: {p1.name}")
print(f"Базовая цена: {p1.price} руб.")
print(f"Цена со скидкой авто: {p1.price_with_discount_auto(date)} руб.")
print("-" * 40)

# Тест 2: Медовик (id=4). Заказов в сентябре НЕ БЫЛО -> должна быть скидка 25%
p2 = Product(4, "Десерт", "Медовик", "Мёд, мука, крем", 450, 8, "medovik.png")
print(f"Блюдо: {p2.name}")
print(f"Базовая цена: {p2.price} руб.")
print(f"Цена со скидкой авто (ожидается 337.5): {p2.price_with_discount_auto(date)} руб.")
