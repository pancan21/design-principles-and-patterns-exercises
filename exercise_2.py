# TODO: The `ShoppingCart` allows for addition of products into it, and finally allows to export
#       the list of products into different file formats - currently xml and json are supported.
#       However, the `ShoppingCart` does not scale well in case exporting into other file formats
#       is to be added, because you have to modify the class for each new file format by adding a
#       new export function. Over time this may lead to the class blowing up. Also, the current
#       implementation violates the DRY principle...
#       To solve these issues, we want to use dependency injection, injecting (for instance) a
#       `ShoppingCartWriter` into a generic `export` function. Thus, usage may look like this,
#       for instance:
#
#       cart = ShoppingCart()
#       # add products...
#       cart.export(XMLShoppingCartWriter(filename="cart.xml"))
#
#       This way, it is possible to export a shopping cart into new data formats without having
#       to change the `ShoppingCart` at all. One only has to implement a new writer class for
#       the new format, that fulfills the interface that your `export` function requires.
#
#       Note: in case you were wondering, we ignore product prices here because price handling
#             may have been changed in exercise_1...
from typing import Protocol
from dataclasses import dataclass
from datetime import datetime
from exercise_1 import Product


# TODO: Implement a `ShoppingCartWriter` interface
# class ShoppingCartWriter(Protocol):
#     pass

class ShoppingCart:
    @dataclass
    class _Entry:
        quantity: int
        last_modified: str

    def __init__(self) -> None:
        self._products: dict = {}

    def add(self, product: Product) -> None:
        if product.name not in self._products:
            self._products[product.name] = self._make_new_entry()
        self._products[product.name].quantity += 1
        self._products[product.name].last_modified = self._get_timestamp()

    # TODO: remove export_to_xml and export_to_json and implement an export() function
    #       that accepts (e.g.) a `ShoppingCartWriter` per dependency injection. Define the
    #       `ShoppingCartWriter` interface that you expect using the `Protocol` class from
    #       the `typing` module. Actual implementations of the interface for xml or json
    #       can be put at the end of this file, for instance.
    def export_to_xml(self, filename: str) -> None:
        with open(filename, "w") as xml_file:
            xml_file.write("<Products>\n")
            for name, entry in self._products.items():
                xml_file.write(f"  <Product name=\"{name}\" quantity=\"{entry.quantity}\" last_modified=\"{entry.last_modified}\"/>\n")
            xml_file.write("</Products>\n")

    def export_to_json(self, filename: str) -> None:
        with open(filename, "w") as json_file:
            json_file.write("{")
            json_file.write("\"products\":[")
            for i, (name, entry) in enumerate(self._products.items()):
                json_file.write("," if i > 0 else "")
                json_file.write(f'{{"name":"{name}","quantity":{entry.quantity}, "last_modified":"{entry.last_modified}"}}')
            json_file.write("]}")

    def _make_new_entry(self) -> _Entry:
        return self._Entry(quantity=0, last_modified=self._get_timestamp())

    def _get_timestamp(self) -> str:
        return datetime.now().isoformat()


# TODO: implement XMLWriter and verify that it produces the same as "export_to_xml()"
# class XMLShoppingCartWriter:
#     pass

# Possible solution for a writer for json
# class JSONShoppingCartWriter:
#     pass

if __name__ == "__main__":
    xml_filename = "cart.xml"
    json_filename = "cart.json"

    cart = ShoppingCart()
    cart.add(Product("Laptop", "999.00"))
    cart.add(Product("Keyboard", "10.00"))
    cart.add(Product("Keyboard", "10.00"))
    cart.export_to_xml(xml_filename)
    cart.export_to_json(json_filename)

    # TODO: implement and use the export interface instead, injecting the respective writer
    # cart.export(XMLShoppingCartWriter("cart.xml"))
    # cart.export(JSONShoppingCartWriter("cart.json"))

    for filename in [xml_filename, json_filename]:
        print(f"Content of '{filename}':")
        print(open(filename).read())
