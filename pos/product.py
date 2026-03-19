import datetime

class Product():
	"""
	Represents a product available in the point-of-sale (POS) system.

	A ``Product`` encapsulates identifying and pricing information
	for an item that can be sold within a transaction. Products are
	typically referenced by their Universal Product Code (UPC).

	Attributes
	----------
	upc : str
		Universal Product Code uniquely identifying the product.
	description : str
		Human-readable description of the product.
	price : float
		Unit price of the product.
	"""

	def __init__(self, upc, description, price):
		"""
		Initialize a new Product instance.

		Parameters
		----------
		upc : str
			Universal Product Code uniquely identifying the product.
		description : str
			Textual description of the product.
		price : float
			Unit price of the product.

		Returns
		-------
		None
		"""
		self.upc = upc
		self.description = description
		self.price = price

	def __eq__(self, other):
		"""
		Determine whether this product is equal to another product.

		Parameters
		----------
		other : Product
			Another product instance to compare against.

		Returns
		-------
		bool
			``True`` if UPC, description, and price are identical;
			otherwise ``False``.
		"""
		return self.upc == other.upc and self.description == other.description and self.price == other.price

	def __str__(self):
		"""
		Return a user-friendly string representation of the product.

		Parameters
		----------
		None

		Returns
		-------
		str
			Formatted string containing UPC, description, and price.
		"""
		return str(self.upc) + "; " + self.description + "; " + str(self.price)

	def __repr__(self):
		"""
		Return an unambiguous string representation for debugging.

		Parameters
		----------
		None

		Returns
		-------
		str
			String representation suitable for debugging and recreation.
		"""
		return "Product(%r, %r, %r)" % (self.upc, self.description, self.price)
