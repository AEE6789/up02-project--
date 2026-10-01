"""Проверка класса Product с новыми полями."""
from models import Product

# Создаём один товар вручную (передаём все 7 полей)
p = Product(
    product_id=1,
    category="Кроссовки",
    name="Nike Air Max",
    composition="Кожа, текстиль, резина",
    price=8500,
    quantity=3,
    photo="nike_air.jpg"
)

print(p.info())
print(f"Со скидкой 25%: {p.price_with_discount(25):.2f} руб.")
