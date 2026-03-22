# sale_dao_pickle.py

import os
import pickle
from pos.dao.sale_dao import SaleDAO
from pos.configuration import Configuration

class SaleDAOPickle(SaleDAO):

    # initialize sales dictionary
    def __init__(self, controller):
        self.sales = {}
        self.controller = controller
        self.autosave = Configuration.autosave
        self.filename = Configuration.sales_file

        #loading
        if self.autosave and os.path.exists(self.filename):
            with open(self.filename, "rb") as f: # read binary for pickle
                self.sales = pickle.load(f) # load the sales dictionary from the file
            
            if self.sales:
                self.controller.sales_counter = max(self.sales.keys()) #set the sales counter to the largest sales ID (most recent)

        else:
            self.sales = {} #no existing file or autosave off

    # Returns a specific sale by its sale ID
    def search_sale(self, key):
        return self.sales.get(key)
    
    # adds a new sale using ID as key to the sales dictionary
    def create_sale(self, sale):
        self.sales[sale.id] = sale
        

    # Returns a list of all sales
    def list_sales(self):
        return list(self.sales.values())
    
    def save_changes(self):
        pass
    

