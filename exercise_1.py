# TODO: `Product` violates both the SRP & DRY principle.
#       Identify where the violations occur and discuss/implement
#       a better solution.
from __future__ import annotations
from decimal import Decimal


class Product:
    def __init__(self, name: str, price: str) -> None:
        self._name = name
        self._price = self._price_from_string(price)

    def __repr__(self) -> str:
        return f"Product: {self._name}, price: {self._price}"

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> Decimal:
        return self._price

    def reduced(self, percentage: int) -> Product:
        assert percentage >= 0 and percentage <= 100
        assert not self._is_reduced()
        reduced_fraction = self._price_from_string(str(percentage))/Decimal("100")
        reduction = self._price*reduced_fraction
        reduction = reduction.quantize(Decimal("1.00"))
        return Product(
            name=f"{self._name} (reduced)",
            price=str(self._price - reduction)
        )

    def _price_from_string(self, price_str: str) -> Decimal:
        if "." not in price_str:
            return Decimal(f"{price_str}.00")
        elif len(price_str.split(".")[1]) != 2:
            raise IOError("Too many decimal digits")
        return Decimal(price_str)

    def _is_reduced(self) -> bool:
        return "(reduced)" in self._name


if __name__ == "__main__":
    print(Product("Laptop", "999.00"))
    print(Product("Laptop", "999.00").reduced(30))
