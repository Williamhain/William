# product_dao_json.py

from pos.dao.product_dao import ProductDAO

class ProductDAOJSON(ProductDAO):

    # initialize product dictionary
    def __init__(self):
        self.products = {}

    # Returns product along with its respective key if found, otherwise returns None
    def search_product(self, key):
        return self.products.get(key)
    
    # Returns False if product with the same UPC already exists, otherwise creates a new product with associated UPC
    def create_product(self, product):
        if product.upc in self.products:
            return False
        else:
            self.products[product.upc] = product
            return True
    
    # Returns a list of products that have descriptions that contain the search string
    def retrieve_products(self, search_string):
        product_list = []

        for product in self.products.values():
            if search_string in product.description:
                product_list.append(product)

        return product_list
    
    # Returns False if product to be updated is not in the dictionary, otherwise, updates a product by UPC 
    def update_product(self, key, product):
        if key not in self.products:
            return False
        else: 
            self.products[key] = product
            return True
    
    # returns False if product to be deleted is not in the dictionary, otherwise, removes the product by UPC
    def delete_product(self, key):
        if key not in self.products:
            return False
        else:
            self.products.pop(key)
            return True
    
    # returns a list of all of the products
    def list_products(self):
        return list(self.products.values())


