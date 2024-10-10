from __future__ import annotations
from decimal import Decimal


class Money:
    def __init__(self, amount: str) -> None:
        self._amount = Decimal(self._format_amount(amount))

    def __repr__(self) -> str:
        return str(self._amount)

    def __add__(self, other: Money) -> Money:
        return Money(str(self._amount + other._amount))

    def __sub__(self, other: Money) -> Money:
        return Money(str(self._amount - other._amount))

    def __mul__(self, value: float) -> Money:
        result = self._round_to_valid_amount(self._amount * Decimal(value))
        return Money(str(result))

    def __truediv__(self, value: float) -> Money:
        result = self._round_to_valid_amount(self._amount / Decimal(value))
        return Money(str(result))

    def _format_amount(self, money_str: str) -> str:
        if "." not in money_str:
            return f"{money_str}.00"
        elif len(money_str.split(".")[1]) != 2:
            raise IOError("Too many decimal digits")
        return money_str

    def _round_to_valid_amount(self, value: Decimal) -> Decimal:
        return value.quantize(Decimal("1.00"))


class Discount:
    def __init__(self, percentage: float) -> None:
        assert 0 <= percentage <= 100, "Discount must be between 0 and 100"
        self._percentage = percentage

    def apply(self, price: Money) -> Money:
        reduction = price * (self._percentage / 100)
        return price - reduction


class Product:
    def __init__(self, name: str, price: str) -> None:
        self._name = name
        self._price = Money(price)

    def __repr__(self) -> str:
        return f"Product: {self._name}, price: {self._price}"

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> Money:
        return self._price

    def reduced(self, percentage: float) -> Product:
        assert not self._is_reduced()
        reduced_price = Discount(percentage).apply(self._price)
        return Product(
            name=f"{self._name} (reduced)",
            price=str(reduced_price)
        )

    def _is_reduced(self) -> bool:
        return "(reduced)" in self._name


if __name__ == "__main__":
    print(Product("Laptop", "999.00"))
    print(Product("Laptop", "999.00").reduced(30))
