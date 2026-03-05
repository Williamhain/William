# controller.py
from pos.product import Product

class Controller:
    def __init__(self):
        self._logged_in = False #set log-in flag initially to false (user is not logged in)
        self._products = {} #UPO code for product

    def logout(self):
        if not self._logged_in: #if not logged in, do nothing
            return False #logout fails because user isn't logged in
        self._logged_in = False #set to logged out
        return True #succesfully completed the self.assertTrue(self.controller.logout())
    
    def login(self, username, password):

        if self._logged_in: #already logged in
            return False #login attempt fails because user is already logged in

        if username == "user" and password == "pos2026": #should be user, not "theuser"
            self._logged_in = True #user is now logged in successfully
            return True #login succeeds
        return False #login fails because of incorrect username or password
    
    def create_product(self, upc, product_name, price):
        if not self._logged_in:
            return None #return None if not logged in
        
        if upc in self._products: #check if the product with the same UPC already exists
            return None #if the product already exists, do nothing and return None
        
        product = Product(upc, product_name, price) #create a new object of type Product
        self._products[upc] = product #assign the product in the dictionary tied to a specific UPC
        return product #function successfully completed, return the newly created product
    
    def search_product(self, upc): #search for a specific product by UPC
        return self._products.get(upc) #return the product if found, otherwise return None
