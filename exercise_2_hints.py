# HINT1:
# A possible solution for your export function could look like this:
# def export(self, writer: ShoppingCartWriter) -> None:
#     for name, entry in self._products.items():
#         writer.add_product_specs(
#             name=name,
#             quantity=entry.quantity,
#             last_modified=entry.last_modified
#         )
#
# using the following ShoppingCartWriter interface:
# from typing import Protocol
# class ShoppingCartWriter(Protocol):
#     """Interface for shopping cart writers"""
#     def add_product_specs(self, *, name: str, **kwargs) -> None:
#         """Insert a product, given its name and an arbitrary number of additional key-value pairs"""
#         ...




# HINT2:
# The skeleton for the xml writer may look like this:
# class XMLShoppingCartWriter:
#     def __init__(self, filename: str) -> None:
#         self._file = open(filename, "w")
#         # TODO: open outer <Products> element

#     def __del__(self) -> None:
#         # TODO: close outer <Products> element
#         self._file.close()

#     # TODO: implement this
#     def add_product_specs(self, *, name: str, **kwargs) -> None:
#         raise NotImplementedError("XMLWriter.add_product_specs()")




# HINT 3
# Possible solution for a writer for json
# class JSONShoppingCartWriter:
#     def __init__(self, filename: str) -> None:
#         self._file = open(filename, "w")
#         self._empty = True
#         self._write_product_list_begin()

#     def __del__(self) -> None:
#         self._write_product_list_end()
#         self._file.close()

#     def add_product_specs(self, *, name: str, **kwargs) -> None:
#         self._file.write("," if not self._empty else "")
#         self._file.write(f'{{"name":"{name}"')
#         for key, value in kwargs.items():
#             self._file.write(f',"{key}":"{value}"')
#         self._file.write("}")
#         self._empty = False

#     def _write_product_list_begin(self) -> None:
#         self._file.write('{"products":[')

#     def _write_product_list_end(self) -> None:
#         self._file.write("]}")
