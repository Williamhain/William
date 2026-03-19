from pos.sale_line_item import SaleLineItem
from datetime import date, datetime

class Sale():
	"""
	Represents a sale transaction in the point-of-sale (POS) system.

	A ``Sale`` aggregates multiple ``SaleLineItem`` objects and maintains
	transaction-level financial information such as totals and taxes.
	The class supports creation, retrieval, and basic computation of
	sale-related data.

	Attributes
	----------
	id : int or None, optional
		Unique identifier of the sale. Defaults to ``None``.
	date : datetime.date or datetime.datetime or None, optional
		Date associated with the sale transaction. Defaults to ``None``.
	total : float, optional
		Precomputed subtotal amount of the sale before taxes. Defaults to 0.00.
	gst : float, optional
		Goods and Services Tax applied to the sale. Defaults to 0.00.
	pst : float, optional
		Provincial Sales Tax applied to the sale. Defaults to 0.00.
	customer_total : float, optional
		Final total amount charged to the customer (including taxes).
		Defaults to 0.00.
	counter : int
		Internal counter used to assign unique codes to sale line items.
	sale_line_items : list of SaleLineItem
		Collection of line items associated with the sale.
	sale_receipt : str
		Formatted receipt text for the sale.
	"""

	def __init__(self, id=None, date=None, total=0.00, gst=0.00, pst=0.00, customer_total=0.00):
		"""
		Initialize a new Sale instance.

		Parameters
		----------
		id : int or None
			Unique identifier of the sale.
		date : datetime.date or datetime.datetime or None
			Date of the sale transaction.
		total : float
			Subtotal amount before taxes.
		gst : float
			Goods and Services Tax amount.
		pst : float
			Provincial Sales Tax amount.
		customer_total : float
			Total amount charged to the customer including taxes.

		Returns
		-------
		None
		"""
		self.counter = 0
		self.sale_line_items = []

		self.id = id
		self.date = date
		self.total = total
		self.gst = gst
		self.pst = pst
		self.customer_total = customer_total
		self.sale_receipt = ""

	def __eq__(self, other):
		"""
		Determine whether this sale is equal to another sale.

		Parameters
		----------
		other : Sale
			Another sale instance to compare against.

		Returns
		-------
		bool
			``True`` if all comparable attributes are equal; otherwise ``False``.
		"""
		return self.id == other.id and self.date == other.date and self.total == other.total \
			and self.gst == other.gst and self.pst == other.pst and self.customer_total == other.customer_total

	def __str__(self):
		"""
		Return a user-friendly string representation of the sale.

		Parameters
		----------
		None

		Returns
		-------
		str
			Formatted string containing sale identifier, date, and monetary values.
		"""
		return f"{self.id}" + "; " + str(self.date) + "; " + f"{self.total:.2f}" \
			+ "; " + f"{self.gst:.2f}" + "; " + f"{self.pst:.2f}" + "; " + f"{self.customer_total:.2f}"

	def __repr__(self):
		"""
		Return an unambiguous string representation for debugging.

		Parameters
		----------
		None

		Returns
		-------
		str
			String that can be used to recreate the object in debugging contexts.
		"""
		return "Sale(%r, %r, %r, %r, %r, %r)" % (self.id, self.date, self.total, self.gst, self.pst, self.customer_total)
	
	def get_number_sale_line_items(self):
		"""
		Return the number of sale line items in the sale.

		Parameters
		----------
		None

		Returns
		-------
		int
			Number of sale line items currently associated with the sale.
		"""
		return self.counter

	def search_sale_line_item(self, code):
		"""
		Search for a sale line item by its code.

		Parameters
		----------
		code : int
			Unique identifier of the sale line item.

		Returns
		-------
		SaleLineItem or None
			Matching sale line item if found; otherwise ``None``.
		"""
		for sale_line_item in self.sale_line_items:
			if sale_line_item.code == code:
				return sale_line_item
		return None

	def create_sale_line_item(self, quantity, price, upc):
		"""
		Create and add a new sale line item to the sale.

		Parameters
		----------
		quantity : int or float
			Quantity of the product being sold.
		price : float
			Unit price of the product.
		upc : str
			Universal Product Code identifying the product.

		Returns
		-------
		SaleLineItem
			The newly created sale line item instance.
		"""
		self.counter += 1
		new_sale_line_item = SaleLineItem(self.counter, quantity, price, upc)
		self.sale_line_items.append(new_sale_line_item)
		return new_sale_line_item

	def retrieve_sale_line_items(self, search_string):
		"""
		Retrieve sale line items that match a search string.

		Parameters
		----------
		search_string : str
			Substring used to filter sale line items.

		Returns
		-------
		list of SaleLineItem
			List of sale line items whose attributes contain the search string.
		"""

		retrieved_sale_line_items = []
		for sale_line_item in self.sale_line_items:
			if search_string in sale_line_item.title or search_string in sale_line_item.text:
				retrieved_sale_line_items.append(sale_line_item)
		return retrieved_sale_line_items

	def list_sale_line_items(self):
		"""
		Return all sale line items in insertion order.

		Parameters
		----------
		None

		Returns
		-------
		list of SaleLineItem
			List containing all sale line items associated with the sale.
		"""
		sale_line_items_list = []
		for i in range(len(self.sale_line_items)):
			sale_line_items_list.append(self.sale_line_items[i])
		return sale_line_items_list
	
	def compute_sale_total(self):
		"""
		Compute the subtotal of the sale based on its line items.

		Parameters
		----------
		None

		Returns
		-------
		float
			Sum of quantity multiplied by price for each sale line item,
			rounded to two decimal places per item.
		"""
		total = 0.0
		for sale_line_item in self.sale_line_items:
			total += round(sale_line_item.quantity * sale_line_item.price, 2)
		return total

	def set_sale_receipt(self, sale_receipt):
		"""
		Set the formatted receipt text for the sale.

		Parameters
		----------
		sale_receipt : str
			Formatted receipt content.

		Returns
		-------
		None
		"""
		self.sale_receipt = sale_receipt

	def get_sale_receipt(self):
		"""
		Return the formatted receipt text for the sale.

		Parameters
		----------
		None

		Returns
		-------
		str
			Receipt text associated with the sale.
		"""
		return self.sale_receipt