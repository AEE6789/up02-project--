"""Модели данных для проекта УП.02."""


class Product:
    """Класс Товар."""

    def __init__(self, product_id, category, name, composition, price, quantity, photo):
        """
        Инициализация товара.

        :param product_id: идентификатор (id)
        :param category: категория
        :param name: название
        :param composition: состав
        :param price: цена
        :param quantity: количество
        :param photo: фото (путь к файлу или ссылка)
        """
        self.id = product_id
        self.category = category
        self.name = name
        self.composition = composition
        self.price = price
        self.quantity = quantity
        self.photo = photo

    def total(self):
        """Общая стоимость (цена × количество)."""
        return self.price * self.quantity

    def price_with_discount(self, discount_percent):
        """Цена со скидкой."""
        return self.price * (1 - discount_percent / 100)

    def indicator(self):
        """Индикатор «много/мало» (порог 5)."""
        return "много" if self.quantity > 5 else "мало"

    def info(self):
        """Строка с информацией о товаре."""
        return (
            f"{self.name} ({self.category}) | Состав: {self.composition}: "
            f"{self.price} руб. × {self.quantity} = {self.total()} руб. "
            f"({self.indicator()})"
        )

class Order:
    """Класс Заказ (отредактирован под новые поля товара)."""

    def __init__(self, order_id, date, client, product, quantity):
        self.id = order_id
        self.date = date
        self.client = client
        self.product = product      # Объект класса Product (содержит ваши 7 полей)
        self.quantity = quantity

    def total(self):
        """Стоимость заказа."""
        return self.product.price * self.quantity

    def info(self):
        """Строка с информацией о заказе с учетом категории и состава товара."""
        return (
            f"Заказ №{self.id} от {self.date}: {self.client} — "
            f"{self.product.name} ({self.product.category}) | "
            f"Состав: {self.product.composition} | "
            f"{self.quantity} шт. на сумму {self.total()} руб."
        )
