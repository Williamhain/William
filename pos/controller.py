# controller.py
from pos.product import Product
from pos.sale import Sale
from pos.sale_line_item import SaleLineItem
from datetime import datetime

class Controller:
    def __init__(self):
        self._logged_in = False #set log-in flag initially to false (user is not logged in)
        self._products = {} #creates an empty dictionary with the UPC code for the product as the key. So, _products will become a long lookup table list of products
        self._current_sale = None
        self._sales = []
        self._sale_counter = 1

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
        actual_product = self._products.get(upc)
        return actual_product #return the product if found, otherwise return None

    def retrieve_products(self, product_name):
        
        if not self._logged_in:
            return None #do not allow user to search for a product if not logged in
        
        retrieved_list = []

        for product in self._products.values(): #look through all products in the dictionary
            if product_name in product.product_name: #check if the searched text is in the product's name
                retrieved_list.append(product) #append the found product to the list

        return retrieved_list 

    def update_product(self, upc, updated_upc, updated_product_name, updated_price):
        
        if not self._logged_in: #do not allow user to update product if not logged in
            return False
        
        product = self.search_product(upc) #search for the product by upc
        if product is None:
            return False #product not found

        if updated_upc != upc: 
            if updated_upc in self._products: 
                return False #if the updated upc is already found in the dictionary (and is not the same as the original upc) then we reject the update
        
        if updated_upc != upc:
            product = self._products.pop(upc) #remove the old UPC 
            self._products[updated_upc] = product #store the product under the new UPC

        product.upc = updated_upc
        product.product_name = updated_product_name
        product.price = updated_price
        return True
    
    def delete_product(self, upc):

        if not self._logged_in: 
            return False #do not allow user to delete product if not logged in 
        
        if upc not in self._products:
            return False #the product is not in the dictionary
            
        del self._products[upc] #delete the specified product by UPC

        return True
    
    def list_products(self):

        if not self._logged_in:
            return None #do not allow user to list the products if not logged in
        
        if len(self._products) == 0:
            return [] #if the list is empty, return an empty list
        
        product_list = []

        for product in self._products.values(): 
            product_list.append(product) #add each product to the list

        return product_list

    #comments
    def initiate_sale(self):
        if not self._logged_in:
            return False #do not allow user to make a sale if not logged in
        
        if self._current_sale is not None:
            return False #if there is already a sale being made, do not start another sale
        
        self._current_sale = Sale(None, None, 0.00, 0.00, 0.00, 0.00) #default current sale

        return True
    
    #comments
    def get_current_sale(self):
        return self._current_sale    
    

    #comments
    def cancel_current_sale(self):

        if not self._logged_in:
            return False

        if self._current_sale is None:
            return False

        self._current_sale = None
        return True
    
    #comments
    def add_sale(self, sale):
        self._sales.append(sale)

    #comments
    def search_sale(self, sale_id):

        if not self._logged_in:
            return None

        for sale in self._sales:
            if sale.sale_id == sale_id:
                return sale

        return None
    
    #comments
    def list_sales(self):

        if not self._logged_in:
            return None

        return self._sales
    
    def create_sale_line_item(self, quantity, price, upc):
        if not self._logged_in or self._current_sale is None:
            return None
            
        #get the auto-incremented code from the current sale
        code = self._current_sale._item_counter
        self._current_sale._item_counter += 1
        
        #create the item and add it to the current sale's list
        new_item = SaleLineItem(code, quantity, price, upc)
        self._current_sale.line_items.append(new_item)
        
        return new_item

    def search_sale_line_item(self, code):
        if not self._logged_in or self._current_sale is None:
            return None
            
        #search through the current sale's line items
        for item in self._current_sale.line_items:
            if item.code == code:
                return item
        return None
    
    #add a new sale line item to the current sale using a product UPC
    def add_new_sale_line_item(self, quantity, upc): 
        if not self._logged_in:
            return None #do not allow to add a new item if user is not logged in
        
        if self._current_sale is None:
            return None #do not allow to add a new item if there is no active current sale
        
        product = self.search_product(upc)
        if product is None:
            return None #if the product doesn't exist in the dictionary, return None
        
        return self.create_sale_line_item(quantity, product.price, upc) #add the created item from the create sale item method to the list of items in the current sale
    
    def get_number_sales(self):
        return len(self._sales) #return the number of sale objects in the list

    def finish_current_sale(self):

        if not self._logged_in:
            return None #user can't finish a sale if they aren't logged in
        
        if self._current_sale is None:
            return None #check if there is no current sale
        
        if self._current_sale.get_number_sale_line_items() == 0:
            return None #can't complete a sale without any line items
        
        subtotal = 0

        for item in self._current_sale.line_items: #loop through all sale line items
            subtotal += item.quantity * item.price #increment subtotal by the quantity of the item multiplied by the price

        subtotal = round(subtotal, 2) #round subtotal to 2 decimal places
        gst = round(subtotal * 0.05, 2) #GST is 5%
        pst = round(subtotal * 0.07, 2) #PST is 7%
        total = round(subtotal + gst + pst, 2) #final total of sale

        sale_id = len(self._sales) + 1 #track each sale made 
        sale_date = datetime.now().date() #today's date
        
        finished_sale = Sale(sale_id, sale_date, subtotal, gst, pst, total) #create final sale object
        self._sales.append(finished_sale) #add sale to list
        self._current_sale = None #set current sale to none now that sale is completed
        return finished_sale
    
    def print_sale_line_item(self, code):

        if not self._logged_in:
            return None
        
        if self._current_sale is None:
            return None #check if there is no current sale
        
        sale_line_item = self.search_sale_line_item(code) #look for the sale line item
        if sale_line_item is None:
            return None #sale line item not found
        
        product = self.search_product(sale_line_item.upc) #find corresponding product
        description = product.product_name #get the product description 
        subtotal = round(sale_line_item.quantity * sale_line_item.price, 2)

        # the dash in %-30s left-aligns the text. the 6 in %6.2f is for 6 spaces to keep allignment with each sale item 
        return "%-30s - %6.2f x %6.2f - %6.2f\n" % (description, sale_line_item.quantity, sale_line_item.price, subtotal)
    
    


