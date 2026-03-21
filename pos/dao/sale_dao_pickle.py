# sale_dao_pickle.py

from pos.dao.sale_dao import SaleDAO

class SaleDAOPickle(SaleDAO):

    # initialize sales dictionary
    def __init__(self, controller):
        self.sales = {}
        self.controller = controller

    # Returns a specific sale by its sale ID
    def search_sale(self, key):
        return self.sales.get(key)
    
    # adds a new sale using ID as key to the sales dictionary
    def create_sale(self, sale):
        self.sales[sale.id] = sale

    # Returns a list of all sales
    def list_sales(self):
        return list(self.sales.values())
    
