# sale_line_item.py

class SaleLineItem:
    def __init__(self, code, quantity, price, upc):
        self.code = code
        self.quantity = quantity
        self.price = price
        self.upc = upc

    def __eq__(self, other):
        if not isinstance(other, SaleLineItem):
            return False
        return (self.code == other.code and 
                self.quantity == other.quantity and 
                self.price == other.price and 
                self.upc == other.upc) 