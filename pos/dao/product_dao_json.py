# product_dao_json.py
import os
import json
from pos.dao.product_dao import ProductDAO
from pos.dao.product_encoder import ProductEncoder
from pos.dao.product_decoder import ProductDecoder
from pos.configuration import Configuration

class ProductDAOJSON(ProductDAO):

    # initialize product dictionary
    def __init__(self):
        self.products = {}
        self.autosave = Configuration.autosave
        self.filename = Configuration.products_file

        if self.autosave and os.path.exists(self.filename):
                with open(self.filename, "r") as f:
                    # using cls=ProductDecoder to match the class inheritance
                    product_list = json.load(f, cls=ProductDecoder)
                    for product in product_list:
                        self.products[product.upc] = product

    def save_to_file(self):
        if self.autosave:
            with open(self.filename, "w") as f:
                json.dump(list(self.products.values()), f, cls=ProductEncoder)

    # Returns product along with its respective key if found, otherwise returns None
    def search_product(self, key):
        return self.products.get(key)
    
    # Returns False if product with the same UPC already exists, otherwise creates a new product with associated UPC
    def create_product(self, product):
        if product.upc in self.products:
            return False
        else:
            self.products[product.upc] = product
            self.save_to_file()
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
            self.save_to_file()
            return True
    
    # returns False if product to be deleted is not in the dictionary, otherwise, removes the product by UPC
    def delete_product(self, key):
        if key not in self.products:
            return False
        else:
            self.products.pop(key)
            self.save_to_file()
            return True
    
    # returns a list of all of the products
    def list_products(self):
        return list(self.products.values())


