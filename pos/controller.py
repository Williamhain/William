import hashlib
from datetime import date, datetime
from pos.product import Product
from pos.sale import Sale
from pos.sale_line_item import SaleLineItem
from pos.configuration import Configuration
from pos.dao.product_dao import ProductDAO
from pos.dao.product_dao_json import ProductDAOJSON
from pos.dao.sale_dao import SaleDAO
from pos.dao.sale_dao_pickle import SaleDAOPickle
from pos.exception.invalid_login_exception import InvalidLoginException
from pos.exception.duplicate_login_exception import DuplicateLoginException
from pos.exception.invalid_logout_exception import InvalidLogoutException
from pos.exception.illegal_access_exception import IllegalAccessException
from pos.exception.illegal_operation_exception import IllegalOperationException
from pos.exception.no_current_sale_exception import NoCurrentSaleException
from pos.exception.invalid_product_exception import InvalidProductException

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

	def __init__(self):
		"""
		Initialize a new Controller instance.

		Parameters
		----------
		None

		Returns
		-------
		None
		"""
		self.configuration = Configuration()
		self.autosave = self.configuration.__class__.autosave
		self.filename = self.configuration.__class__.users_file

		self.username = None
		self.password = None
		self.logged = False

		self.product_dao = ProductDAOJSON()

		self.sales_counter = 0
		self.sale_dao = SaleDAOPickle(self)

		self.current_sale = None

		if self.autosave:
			self.users = self.load_users()
		else:
			self.users = \
			{"user":"8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92", \
			"ali":"6394ffec21517605c1b426d43e6fa7eb0cff606ded9c2956821c2c36bfee2810", \
			"kala":"e5268ad137eec951a48a5e5da52558c7727aaa537c8b308b5e403e6b434e036e"}


	def load_users(self):
		users = {}
		with open(self.filename, 'r') as file:
			for line in file:
				tokens = line.strip().split(',')
				users[tokens[0]] = tokens[1]
		return users


	def get_password_hash(self, password):
		encoded_password = password.encode('utf-8')     # Convert the password to bytes
		hash_object = hashlib.sha256(encoded_password)      # Choose a hashing algorithm (e.g., SHA-256)
		hex_dig = hash_object.hexdigest()       # Get the hexadecimal digest of the hashed password
		return hex_dig


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
			raise DuplicateLoginException("Cannot login more than once in this system.")
		if self.users.get(username):
			password_hash = self.get_password_hash(password)
			if password_hash == self.users.get(username):
				self.username = username
				self.password = password
				self.logged = True
				return True
			else:
				raise InvalidLoginException("Invalid username or password.")
		else:
			raise InvalidLoginException("Invalid username or password.")

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
			raise InvalidLogoutException("Cannot logout without logging in first.")			
		else:
			self.username = None
			self.password = None
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
			raise IllegalAccessException("Illegal Access: Must login first.")

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
			raise IllegalAccessException("Illegal Access: Must login first.")

		# product already exists, do not create them
		if self.search_product(upc):
			raise IllegalOperationException("Illegal Operation: Cannot add a product with an UPC that is already registered.")

		# finally, create a new product
		product = Product(upc, description, price)
		return self.product_dao.create_product(product)
	

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
			raise IllegalAccessException("Illegal Access: Must login first.")

		return self.product_dao.retrieve_products(description)

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
			raise IllegalAccessException("Illegal Access: Must login first.")

		# first, search the product by key
		product = self.search_product(original_upc)

		# product does not exist, cannot update
		if not product:
			raise IllegalOperationException("Illegal Operation: Cannot update an inexistent product.")

		# new upc is used by existing product, cannot update
		if original_upc != upc:
			if self.search_product(upc):
				raise IllegalOperationException("Illegal Operation: Cannot update a product with a new UPC that is already registered.")

		product = Product(upc, description, price)
		return self.product_dao.update_product(original_upc, product)
			
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
			raise IllegalAccessException("Illegal Access: Must login first.")

		# first, search the product by key
		product = self.search_product(upc)

		# product does not exist, cannot delete
		if not product:
			raise IllegalOperationException("Illegal Operation: Cannot delete an inexistent product.")

		# product exists, delete product
		return self.product_dao.delete_product(upc)
	
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
			raise IllegalAccessException("Illegal Access: Must login first.")

		return self.product_dao.list_products()

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
			raise IllegalAccessException("Illegal Access: Must login first.")

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
			raise IllegalAccessException("Illegal Access: Must login first.")

		return self.sale_dao.list_sales()

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
			raise IllegalAccessException("Illegal Access: Must login first.")
		
		# there is a current sale is current sale, cannot update
		if self.current_sale:
			raise IllegalOperationException("cannot initiate sale with a sale in progress")
		
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
			raise IllegalAccessException("Illegal Access: Must login first.")
		
		# there is no current sale to be cancelled, cannot cancel
		if not self.current_sale:
			raise NoCurrentSaleException("cannot cancel sale without initiating it first")
		
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
			raise IllegalAccessException("Illegal Access: Must login first.")
		
		# there is no current sale to add sale line item, cannot add
		if not self.current_sale:
			raise NoCurrentSaleException("cannot add sale new line item without a valid current sale")
		
		# check whether the product is valid before adding the sale line item
		product = self.search_product(upc)
		if not product:
			raise InvalidProductException("Invalid Product: Must be a valid UPC registered in the system.")
		
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
			raise IllegalAccessException("Illegal Access: Must login first.")
		
		# there is no current sale to be finished, cannot finish
		if not self.current_sale:
			raise NoCurrentSaleException("cannot finish sale without initiating it first")
		
		# cannot finish current sale with no sale line items
		if self.current_sale.get_number_sale_line_items() == 0:
			raise IllegalOperationException("cannot finish a sale without items")

		# set the relevant fields in the current sale
		self.sales_counter += 1
		self.current_sale.id = self.sales_counter
		self.current_sale.date = datetime.now().date()
		self.current_sale.total = round(self.current_sale.compute_sale_total(), 2)
		self.current_sale.gst = round(0.05 * self.current_sale.total, 2)
		self.current_sale.pst = round(0.07 * self.current_sale.total, 2) 
		self.current_sale.customer_total = round(self.current_sale.total + self.current_sale.gst + self.current_sale.pst, 2)
		# store the sale receipt
		self.current_sale.set_sale_receipt(self.print_sale_receipt())

		# add the current sale to the sales collection
		self.sale_dao.create_sale(self.current_sale)
		
		# finish current sale and return the sale with success
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
			raise IllegalAccessException("Illegal Access: Must login first.")
		
		# there is no current sale to be printed, cannot print
		if not self.current_sale:
			raise NoCurrentSaleException("cannot print sale receipt without a valid current sale")
		
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
			raise IllegalAccessException("Illegal Access: Must login first.")

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
			raise IllegalAccessException("Illegal Access: Must login first.")

		# there must be a valid current sale
		if not self.current_sale:
			raise NoCurrentSaleException("cannot print sale line items without a valid current sale")

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
			raise IllegalAccessException("Illegal Access: Must login first.")

		# there must be a valid current sale
		if not self.current_sale:
			raise NoCurrentSaleException("cannot search sale line item without a valid current sale")

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
			raise IllegalAccessException("Illegal Access: Must login first.")

		# there must be a valid current sale
		if not self.current_sale:
			raise NoCurrentSaleException("cannot create sale line items without a valid current sale")

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
			raise IllegalAccessException("Illegal Access: Must login first.")

		# there must be a valid current sale
		if not self.current_sale:
			raise NoCurrentSaleException("cannot print sale line item without a valid current sale")

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