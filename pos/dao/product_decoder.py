from json import JSONDecoder
from pos.product import Product

class ProductDecoder(JSONDecoder):
  def __init__(self, *args, **kwargs):
    super().__init__(object_hook=self.object_hook, *args, **kwargs)

  def object_hook(self, dct):
    if '__type__' in dct and dct['__type__'] == 'Product':
      return Product(dct['upc'], dct['description'], dct['price'])
    return dct
