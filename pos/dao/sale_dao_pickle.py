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

        self.load_from_file()

    def load_from_file(self):
        # loads sales from file if autosave is on and if file eists
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
        self.save_changes() 
        

    # Returns a list of all sales
    def list_sales(self):
        return list(self.sales.values())
    
    # saves sales to files using pickle if autosave is on
    def save_changes(self):
        if self.autosave:
            with open(self.filename, "wb") as f: # write binary to overwrite the file
                pickle.dump(self.sales, f) #write the sales dictionary to the file
        else:
            pass # no autosave, do nothing
