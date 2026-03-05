# product.py

class Product:
    def __init__(self, upc, product_name, price):
        self.upc = upc
        self.product_name = product_name
        self.price = price

    def __eq__(self, other):
        return (self.upc == other.upc and self.product_name == other.product_name and self.price == other.price) #otherwise, return true if the UPC, name, and price match (a duplicate product)