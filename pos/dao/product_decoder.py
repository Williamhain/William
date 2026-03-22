# product_decoder.py
import json
from pos.product import Product

class ProductDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        #pass the custom object_hook to the parent JSONDecoder class
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        #check if the dictionary represents a Product
        if "__type__" in obj and obj["__type__"] == "Product":
            return Product(obj["upc"], obj["description"], obj["price"])
        return obj