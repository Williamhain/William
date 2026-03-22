# product_encoder.py
import json
from pos.product import Product

class ProductEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Product):
            return {
                "__type__": "Product",
                "upc": obj.upc,
                "description": obj.description,
                "price": obj.price
            }
        return super().default(obj)