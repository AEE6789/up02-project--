"""Модели данных для проекта УП.02 (Кулинария)."""
from datetime import datetime
from discount import calculate_price_with_discount


class Product:
    """Класс Товар (Блюдо)."""

    def __init__(self, product_id, category, name, composition, price, quantity, photo):
        """Инициализация товара с 7 полями вашей БД."""
        self.id = product_id
        self.category = category
        self.name = name
        self.composition = composition
        self.price = price
        self.quantity = quantity
        self.photo = photo

    def total(self):
        """Общая стоимость остатка блюда."""
        return self.price * self.quantity

    def price_with_discount_auto(self, date=None):
        """Цена со скидкой по алгоритму ДЭ."""
        if date is None:
            date = datetime.now()
        return calculate_price_with_discount(self.id, self.price, date)

    def indicator(self):
        """Индикатор остатка."""
        return "много" if self.quantity > 5 else "мало"

    def is_available(self):
        """Есть ли в наличии."""
        return self.quantity > 0

    def info(self):
        """Информация о блюде."""
        return (
            f"{self.name} ({self.category}) | Состав: {self.composition}: "
            f"{self.price} руб. × {self.quantity} = {self.total()} руб. "
            f"({self.indicator()})"
        )


class Order:
    """Класс Заказ."""

    def __init__(self, order_id, date, client, product, quantity):
        self.id = order_id
        self.date = date
        self.client = client
        self.product = product  # Объект класса Product
        self.quantity = quantity

    def total(self):
        return self.product.price * self.quantity

    def info(self):
        return (
            f"Заказ №{self.id} от {self.date}: {self.client} — "
            f"{self.product.name} × {self.quantity} шт."
        )

