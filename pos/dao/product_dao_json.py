import os
from pos.configuration import Configuration
from pos.dao.product_dao import ProductDAO
from pos.product import Product

from pos.dao.product_encoder import ProductEncoder
from pos.dao.product_decoder import ProductDecoder
from json import loads, dumps

class ProductDAOJSON(ProductDAO):

	def __init__(self):
		self.configuration = Configuration()
		self.autosave = self.configuration.__class__.autosave
		self.filename = self.configuration.__class__.products_file

		if self.autosave:

			self.products = {}
			try:
				with open(self.filename, 'r') as file:
					for product_json in file:
						product = loads(product_json, cls=ProductDecoder)
						 
						self.products[product.upc] = product
			except:
				pass
		else:
			self.products = {}

	def search_product(self, key):
		return self.products.get(key)

	def create_product(self, product):
		self.products[product.upc] = product

		# if persistence is set, save all products
		if self.autosave:
			with open(self.filename, 'w') as file:
				for key in self.products:
					product_json = dumps(self.products[key], cls=ProductEncoder)
					file.write('%s\n' % (product_json))

		return product

	def retrieve_products(self, search_string):
		retrieved_products = []
		# convert search term to lowercase and remove spaces
		search_lower = search_string.strip().lower()

		for product in self.products.values():
			# startswith() ensures we only match from the beginning, not the middle
			if product.description.lower().startswith(search_lower):
				retrieved_products.append(product)
		return retrieved_products

	def update_product(self, key, product):

		# treat different keys as a separate case
		if key != product.upc:
			self.products.pop(key)
		self.products[product.upc] = product

		# if persistence is set, save all products
		if self.autosave:
			with open(self.filename, 'w') as file:
				for key in self.products:
					product_json = dumps(self.products[key], cls=ProductEncoder)
					file.write('%s\n' % (product_json))

		return True

	def delete_product(self, key):
		# product exists, delete product
		self.products.pop(key)

		# if persistence is set, save all products
		if self.autosave:
			with open(self.filename, 'w') as file:
				for key in self.products:
					product_json = dumps(self.products[key], cls=ProductEncoder)
					file.write('%s\n' % (product_json))

		return True

	def list_products(self):
		products_list = []
		for product in self.products.values():
			products_list.append(product)
		return products_list
