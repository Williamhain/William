# controller.py
from pos.product import Product

class Controller:
    def __init__(self):
        self._logged_in = False #set log-in flag initially to false (user is not logged in)
        self._products = {} #creates an empty dictionary with the UPC code for the product as the key. So, _products will become a long lookup table list of products

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

    def update_product(self, upc, updated_upc, updated_product_name, updated_price):
        
        if not self._logged_in: #do not allow user to update product if not logged in
            return False
        
        if upc not in self._products: #do not allow user to update a product that doesn't exist
            return False
        
        if updated_upc != upc and updated_upc in self._products: #if the updated upc is already found in the dictionary (and is not the same as the original upc) then we reject the update
            return False 
        
        updated_product = Product(updated_upc, updated_product_name, updated_price) #create a new Product object with updated upc, product name, and price
        self._products[updated_upc] = updated_product #store the updated product in the dictionary with the UPC as the key

        if updated_upc != upc: #check if the upc was changed
            del self._products[upc] #if the upc was changed, delete the original upc code

        return True
    

