from datetime import date, datetime
from pos.product import Product
from pos.sale import Sale
from pos.sale_line_item import SaleLineItem
from pos.dao.product_dao_json import ProductDAOJSON
from pos.dao.sale_dao_pickle import SaleDAOPickle
from pos.exception.illegal_access_exception import IllegalAccessException
from pos.exception.illegal_operation_exception import IllegalOperationException
from pos.exception.invalid_product_exception import InvalidProductException
from pos.exception.invalid_login_exception import InvalidLoginException
from pos.exception.duplicate_login_exception import DuplicateLoginException
from pos.exception.invalid_logout_exception import InvalidLogoutException
from pos.exception.no_current_sale_exception import NoCurrentSaleException

import hashlib
import os

class Controller():
	"""
	Coordinates operations within the point-of-sale (POS) system.

	The ``Controller`` acts as the application-layer façade responsible
	for managing sales and products. It mediates between client code
	(e.g., user interface or tests) and the underlying domain entities
	(``Sale``, ``Product``), ensuring consistent creation, retrieval,
	and management of transactional data.

	Attributes
	----------
	sales : list of Sale
		Collection of sales managed by the controller.
	products : list of Product
		Collection of products available in the system.
	sale_counter : int
		Internal counter used to assign unique identifiers to sales.
	"""

	def __init__(self, autosave=False):
		"""
		Initialize a new Controller instance.

		Parameters
		----------
		None

		Returns
		-------
		None
		"""
		from pos.configuration import Configuration
		self.autosave = autosave or Configuration.autosave
		self.users = {}
		
		if self.autosave and os.path.exists(Configuration.users_file):
			with open(Configuration.users_file, "r") as f:
				for line in f:
					line = line.strip()
					if line:
						parts = line.split() 
						if len(parts) >= 2:
							self.users[parts[0]] = parts[1]
		else:
			# hard code users passwords in, change later
			self.users = {
				"user": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92",
				"ali": "6394ffec21517605c1b426d43e6fa7eb0cff606ded9c2956821c2c36bfee2810",
				"kala": "e5268ad137eec951a48a5e5da52558c7727aaa537c8b308b5e403e6b434e036e"
			}

		self.username = None
		self.password = None
		self.logged = False

		self.product_dao = ProductDAOJSON()
		self.sale_dao = SaleDAOPickle(self)
		self.current_sale = None
		self.sales_counter = 0

	def login(self, username, password):
		"""
		Authenticate a user and log them into the system.

		Parameters
		----------
		username : str
			Username of the user attempting to log in.
		password : str
			Password corresponding to the username.

		Returns
		-------
		bool
			True if login succeeds; otherwise False.
		"""
		if self.logged:
			raise DuplicateLoginException()
		if username in self.users:
			password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
			if password_hash == self.users[username]:
				self.username = username
				self.password = password
				self.logged = True
				return True
			else:
				raise InvalidLoginException()
		else:
			raise InvalidLoginException()
			
	def logout(self):
		"""
		Log out the current user and reset session state.

		Parameters
		----------
		None

		Returns
		-------
		bool
			True if logout succeeds; otherwise False.
		"""
		if not self.logged:
			raise InvalidLogoutException()
		self.username = self.password = None
		self.logged = False
		self.current_sale = None
		return True

	def search_product(self, upc):
		"""
		Search for a product by its UPC.

		Parameters
		----------
		upc : str
			Universal Product Code to search for.

		Returns
		-------
		Product or None
			The matching product if found; otherwise None.
		"""

		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException("User must be logged in to search products.")
		return self.product_dao.search_product(upc)

	def create_product(self, upc, description, price):
		"""
		Create and register a new product.

		Parameters
		----------
		upc : str
			Universal Product Code of the new product.
		description : str
			Product description.
		price : float
			Unit price of the product.

		Returns
		-------
		Product or None
			The newly created product if successful; otherwise None
			due to login failure or existing product.
		"""
 
 		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException("User must be logged in to create products.")
		# product already exists, do not create them
		if self.product_dao.search_product(upc):
			raise IllegalOperationException()

		# finally, create a new product
		product = Product(upc, description, price)
		self.product_dao.create_product(product)
		return product

	def retrieve_products(self, description):
		"""
		Retrieve products containing a description substring.

		Parameters
		----------
		description : str
			Substring to search within product descriptions.

		Returns
		-------
		list of Product or None
			List of products whose description contains the substring, or None if not logged in.
		"""
 
 		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException("User must be logged in to retrieve products.")
		
		return self.product_dao.retrieve_products(description)

		#retrieved_products = []
		#for product in self.products.values():
		#	if description in product.description:
		#		retrieved_products.append(product)
		#return retrieved_products

	def update_product(self, original_upc, upc, description, price):
		"""
		Update the details of an existing product.

		Parameters
		----------
		original_upc : str
			Original UPC of the product.
		upc : str
			New UPC for the product.
		description : str
			New product description.
		price : float
			New unit price.

		Returns
		-------
		bool
			True if update succeeded; otherwise False.
		"""

		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException("User must be logged in to update products.")

		# first, search the product by key
		product = self.product_dao.search_product(original_upc)

		# product does not exist, cannot update
		if not product:
			raise IllegalOperationException()

		# product exists, update fields
		product.description = description
		product.price = price

		# treat different keys as a separate case


		if original_upc != upc:
			if self.product_dao.search_product(upc):
				raise IllegalOperationException("Cannot update: A product with the new UPC already exists.")
			self.product_dao.delete_product(original_upc)
			product.upc = upc
			self.product_dao.create_product(product)
		else:
			self.product_dao.update_product(original_upc, product)
		return True
			
	def delete_product(self, upc):
		"""
		Delete a product by its UPC.

		Parameters
		----------
		upc : str
			UPC of the product to delete.

		Returns
		-------
		bool
			True if deletion succeeded; otherwise False.
		"""

		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException("User must be logged in to delete products.")

		# first, search the product by key
		product = self.product_dao.search_product(upc)

		# product does not exist, cannot delete
		if not product:
			raise IllegalOperationException()

		# product exists, delete product
		self.product_dao.delete_product(upc)
		return True
	
	def list_products(self):
		"""
		Return all products.

		Returns
		-------
		list of Product or None
			List of all products if logged in; otherwise None.
		"""

		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException("User must be logged in to list products.")

		return self.product_dao.list_products()
	
		#products_list = []
		#for product in self.products.values():
		#	products_list.append(product)
		#return products_list

	def add_sale(self, sale):
		"""
		Helper method to add a sale to the sales collection.

		Parameters
		----------
		sale : Sale
			Sale instance to add.

		Returns
		-------
		None
		"""

		self.sales_counter += 1
		self.sale_dao.create_sale(sale)

	def search_sale(self, id):
		"""
		Search for a sale by ID.

		Parameters
		----------
		id : int
			Identifier of the sale.

		Returns
		-------
		Sale or None
			Sale instance if found; otherwise None.
		"""
  
  		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException()

		return self.sale_dao.search_sale(id)

	def list_sales(self):
		"""
		Return all sales.

		Returns
		-------
		list of Sale or None
			All sales if logged in; otherwise None.
		"""

		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException()

		return self.sale_dao.list_sales()

		#sales_list = []
		#for sale in self.sales.values():
		#	sales_list.append(sale)
		#return sales_list

	def initiate_sale(self):
		"""
		Start a new sale transaction.

		Returns
		-------
		bool
			True if sale initiation succeeds; otherwise False.
		"""
  
		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException()
		
		# there is a current sale is current sale, cannot update
		if self.current_sale:
			raise IllegalOperationException()
		
		# create a sale with default values (null and zero) and make it the current sale
		sale  = Sale()
		self.current_sale = sale
		return True

	def cancel_current_sale(self):
		"""
		Cancel the currently active sale.

		Returns
		-------
		bool
			True if cancellation succeeds; otherwise False.
		"""

		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException()
		
		# there is no current sale to be cancelled, cannot cancel
		if not self.current_sale:
			raise NoCurrentSaleException()
		
		# cancel an existing initiated sale
		self.current_sale = None
		return True

	def add_new_sale_line_item(self, quantity, upc):
		"""
		Add a new line item to the current sale.

		Parameters
		----------
		quantity : float
			Quantity of the product.
		upc : str
			UPC of the product.

		Returns
		-------
		SaleLineItem or None
			The newly created line item if successful; otherwise None.
		"""

		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException()
		
		# there is no current sale to add sale line item, cannot add
		if not self.current_sale:
			raise NoCurrentSaleException()
		
		# check whether the product is valid before adding the sale line item
		product = self.search_product(upc)
		if not product:
			raise InvalidProductException()
		
		# query the product price first 
		price = product.price

		# create a new sale line item with another system operation
		return self.create_sale_line_item(quantity, price, upc)


	def finish_current_sale(self):
		"""
		Finalize the current sale, computing totals and adding it to the sales collection.

		Returns
		-------
		Sale or None
			The finalized sale if successful; otherwise None.
		"""
 
		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException()
		
		# there is no current sale to be cancelled, cannot cancel
		if not self.current_sale:
			raise NoCurrentSaleException()
		
		# cannot finish current sale with no sale line items
		if self.current_sale.get_number_sale_line_items() == 0:
			raise IllegalOperationException()

		# set the relevant fields in the current sale
		self.sales_counter += 1
		self.current_sale.id = self.sales_counter
		self.current_sale.date = datetime.now().date()
		self.current_sale.total = round(self.current_sale.compute_sale_total(), 2)
		self.current_sale.gst = round(0.05 * self.current_sale.total, 2)
		self.current_sale.pst = round(0.07 * self.current_sale.total, 2) 
		self.current_sale.customer_total = round(self.current_sale.total + self.current_sale.gst + self.current_sale.pst, 2)

		# add the current sale to the sales collection
		self.sale_dao.create_sale(self.current_sale)	
		
		# print the sale receipt, finish current sale and return the sale with success
		self.current_sale.set_sale_receipt(self.print_sale_receipt())
		temp = self.current_sale
		self.current_sale = None
		return temp
	

	def print_sale_receipt(self):
		"""
		Generate a formatted string representing the sale receipt.

		Returns
		-------
		str or None
			Formatted sale receipt if a current sale exists with line items; otherwise None.
		"""

		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException()
		
		# there is no current sale to be printed, cannot print
		if not self.current_sale:
			raise NoCurrentSaleException()
		
		# cannot print current sale with no sale line items
		if self.current_sale.get_number_sale_line_items() == 0:
			return None

		# print the sale receipt
		receipt = "MARKET AT VICTORIA - SALES RECEIPT\n\n"
		receipt += f"Sale # {self.current_sale.id}\n\n"
		receipt += "-----------------------------------------------------------\n"
		receipt += "ITEM NAME                      -    QTY x   UNIT - SUBTOTAL\n\n"
		for i in range(self.current_sale.get_number_sale_line_items()):
			receipt += self.print_sale_line_item(i+1)
		receipt += "-----------------------------------------------------------\n"
		receipt += f"NET SALE                                         - {self.current_sale.total:6.2f}\n"
		receipt += f"GST (5%)                                         - {self.current_sale.gst:6.2f}\n"
		receipt += f"PST (7%)                                         - {self.current_sale.pst:6.2f}\n"
		receipt += "-----------------------------------------------------------\n"
		receipt += f"TOTAL SALE                                       - {self.current_sale.customer_total:6.2f}\n"
		return receipt
		 			

	def get_current_sale(self):
		"""
		Return the currently active sale.

		Returns
		-------
		Sale or None
			Current sale if logged in; otherwise None.
		"""

		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException()

		# return current sale
		return self.current_sale

	def print_sale_line_items(self):
		"""
		Return a string representing all sale line items for the current sale.

		Returns
		-------
		str or None
			Formatted string of all line items; None if no current sale or not logged in.
		"""
 
 		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException()

		# there must be a valid current sale
		if not self.current_sale:
			raise NoCurrentSaleException()

		# create the string with the list of sale line items
		print_string = ""
		total_items = self.current_sale.get_number_sale_line_items()
		for i in range(total_items):
			print_string += self.print_sale_line_item(i+1)
		if not print_string:
			return None
		else:
			return print_string

	def search_sale_line_item(self, code):
		"""
		Search for a sale line item in the current sale by code.

		Parameters
		----------
		code : int
			Code/index of the line item to search.

		Returns
		-------
		SaleLineItem or None
			Matching line item if found; otherwise None.
		"""

		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException()

		# there must be a valid current sale
		if not self.current_sale:
			raise NoCurrentSaleException()

		# search a new sale line item with the given code and return it 
		return self.current_sale.search_sale_line_item(code)

	def create_sale_line_item(self, quantity, price, upc):
		"""
		Create a new sale line item and add it to the current sale.

		Parameters
		----------
		quantity : float
			Quantity of the product.
		price : float
			Unit price of the product.
		upc : str
			UPC of the product.

		Returns
		-------
		SaleLineItem or None
			Newly created line item if successful; otherwise None.
		"""

		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException()

		# there must be a valid current sale
		if not self.current_sale:
			raise NoCurrentSaleException()

		# create a new sale line item and return it
		return self.current_sale.create_sale_line_item(quantity, price, upc)
	
	def print_sale_line_item(self, code):
		"""
		Return a formatted string representing a single sale line item.

		Parameters
		----------
		code : int
			Code/index of the line item to print.

		Returns
		-------
		str or None
			Formatted string of the line item; None if invalid or not logged in.
		"""

		# must be logged in to do operation
		if not self.logged:
			raise IllegalAccessException()

		# there must be a valid current sale
		if not self.current_sale:
			raise NoCurrentSaleException()

		# search the sale line item
		sale_line_item = self.search_sale_line_item(code)
		if not sale_line_item:
			return None
		else:
			sale_line_item_string = ""
			sale_line_item_string += f"{self.search_product(sale_line_item.upc).description:<30} - "
			sale_line_item_string += f"{sale_line_item.quantity:6.2f}" + " x " + f"{sale_line_item.price:6.2f}" + " - "
			sale_line_item_string += f"{round(sale_line_item.quantity * sale_line_item.price, 2):6.2f}\n"
			return sale_line_item_string

	def get_number_sales(self):
		"""
		Return the total number of sales added to the system.

		Returns
		-------
		int
			Number of sales.
		"""

		return self.sales_counter
	
	def get_password_hash(self, password):
		encoded_password = password.encode('utf-8') #converts string to bytes for hashing purposes
		hash_object = hashlib.sha256(encoded_password) #create sha-256 hash object using the created bytes
		hex_dig = hash_object.hexdigest() #converts hash to readable hex string
		return hex_dig #returns the final hashed password

