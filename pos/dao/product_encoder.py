from json import JSONEncoder
from pos.product import Product

class ProductEncoder(JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Product):
      return {"__type__": "Product", 
       "upc": obj.upc, "description": obj.description, "price": obj.price}
    return super().default(obj)
