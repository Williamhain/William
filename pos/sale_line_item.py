import datetime

class SaleLineItem():
	"""
	Represents a single line item within a sale transaction.

	A ``SaleLineItem`` encapsulates the quantity and price of a specific
	product identified by its Universal Product Code (UPC). It is used
	by the ``Sale`` class to compute transaction totals and maintain
	itemized purchase information.

	Attributes
	----------
	code : int
		Unique identifier assigned to the sale line item within a sale.
	quantity : int or float
		Quantity of the product being purchased.
	price : float
		Unit price of the product at the time of sale.
	upc : str
		Universal Product Code identifying the product.
	"""

	def __init__(self, code, quantity, price, upc):
		"""
		Initialize a new SaleLineItem instance.

		Parameters
		----------
		code : int
			Unique identifier for the sale line item.
		quantity : int or float
			Quantity of the product.
		price : float
			Unit price of the product.
		upc : str
			Universal Product Code of the product.

		Returns
		-------
		None
		"""
		self.code = code
		self.quantity = quantity
		self.price = price
		self.upc = upc

	def __eq__(self, other):
		"""
		Determine whether this sale line item is equal to another.

		Parameters
		----------
		other : SaleLineItem
			Another sale line item instance to compare against.

		Returns
		-------
		bool
			``True`` if all attributes are equal; otherwise ``False``.
		"""
		return self.code == other.code and self.quantity == other.quantity and self.price == other.price and self.upc == other.upc

	def __str__(self):
		"""
		Return a user-friendly string representation of the sale line item.

		Parameters
		----------
		None

		Returns
		-------
		str
			Formatted string containing code, quantity, price, and UPC.
		"""
		return str(self.code) + "; " + str(self.quantity) + "; " + str(self.price) + "; " + self.upc

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
		return "SaleLineItem(%r, %r, %r, %r)" % (self.code, self.quantity, self.price, self.upc)