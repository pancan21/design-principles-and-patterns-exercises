# Hint 1
# As you can see, `Product` internally uses `Decimal` to represent the price
# in order to ensure that only two digits after the comma are used. This also
# reduces rounding errors when multiplying prices, etc..
# But, the responsibility of `Product` is to store product info. Should it know
# about details of how to represent prices?


# Hint 2
# Put handling of prices into a separate class, e.g. `Money`. This could be created
# from a string and do the checks that are currently in `Product`. Internally it can
# still use use `Decimal`, but it may expose the necessary arithmetic operations on
# money: addition/subtraction with another `Money`, multiplication/division with `float`
# This way users do not have to know that `Decimal` is used under the hood. It is a
# implementation detail.


# Hint 3
# Operators in python:
# class MyType:
#     def __add__(self, other: MyType) -> MyType:    # add other and self
#     def __sub__(self, other: MyType) -> MyType:    # subtract other from self
#     def __mul__(self, value: float) -> MyType:     # multiply self with value
#     def __truediv__(self, value: float) -> MyType: # divide self by value


# Hint 4
# `Money` could be created like this
# class Money:
#     def __init__(self, amount: str) -> None:
#         self._amount = Decimal(self._format_amount(amount))
#
#     def _format_amount(self, money_str: str) -> str:
#         if "." not in money_str:
#             return f"{money_str}.00"
#         elif len(money_str.split(".")[1]) != 2:
#             raise IOError("Too many decimal digits")
#         return money_str


# Hint 5
# `Money` instances could be added like this
# class Money:
#     def __repr__(self) -> str:
#         """Return the string representation of the amount of money"
#         return str(self._amount)
#
#     def __add__(self, other: Money) -> Money:
#         # reuse addition of two `Decimal` and our constructor from a string
#         return Money(str(self._amount + other._amount))


# Hint 6
# `Money` instances could be multiplied with a float like this
# class Money:
#     def __mul__(self, value: float) -> Money:
#         result = self._round_to_valid_amount(
#             self._amount*Decimal(value)
#         )
#         return Money(str(result))
#
#     def _round_to_valid_amount(self, value: Decimal) -> Decimal:
#             return value.quantize(Decimal("1.00"))


# Hint 7
# The `reduced` function receives the price reduction as a float in percent, and it then
# checks if the value is in the valid range for a reduction - between 0 and 100 since they
# don't want to reduce prices by more than by 100%. In any other place in our system
# where we want to deal with discounts, we would have to repeat such thing. To consolidate
# this knowledge into a single place, and to be able to write more type-safe interfaces,
# we may introduce a `Discount` class that can be constructed from a percentage, which we
# then pass into the `reduced` function.
