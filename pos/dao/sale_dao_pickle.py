import os
import datetime
from pickle import load, dump
from pos.dao.sale_dao import SaleDAO
from pos.sale import Sale
from pos.configuration import Configuration

class SaleDAOPickle(SaleDAO):

	def __init__(self, controller):

		self.configuration = Configuration()
		self.autosave = self.configuration.__class__.autosave
		self.filename = self.configuration.__class__.sales_file

		if self.autosave:
			try:
				with open(self.filename, 'rb') as file:
					self.sales = load(file)
					controller.sales_counter = list(self.sales.keys())[-1]
			except:
				self.sales = {}
		else:
			self.sales = {}

	def search_sale(self, key):
		return self.sales.get(key)
 
	def create_sale(self, sale):
		self.sales[sale.id] = sale

		# if persistence is set, save all sales
		if self.autosave:
			with open(self.filename, 'wb') as file:
				dump(self.sales, file)
				
		return sale

	def list_sales(self):
 		# list existing sales
		sales_list = []
		for key in self.sales:
			sales_list.append(self.sales[key])
		return sales_list
