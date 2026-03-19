from unittest import TestCase
from unittest import main
from pos.sale_line_item import SaleLineItem
import datetime

class SaleLineItemTest(TestCase):
	def setUp(self):
		self.sale_line_item = SaleLineItem(1, 2, 4.99, "037466022680")

	def test_eq(self):
		same_sale_line_item = SaleLineItem(1, 2, 4.99, "037466022680")
		different_sale_line_item_1 = SaleLineItem(1, 2, 4.99, "629070500083")
		different_sale_line_item_2 = SaleLineItem(1, 3, 4.99, "037466022680")
		different_sale_line_item_3 = SaleLineItem(1, 2, 4.50, "037466022680")
		self.assertTrue(self.sale_line_item == self.sale_line_item)
		self.assertTrue(self.sale_line_item == same_sale_line_item)
		self.assertFalse(self.sale_line_item == different_sale_line_item_1)
		self.assertFalse(self.sale_line_item == different_sale_line_item_2)
		self.assertFalse(self.sale_line_item == different_sale_line_item_3)

	def test_str(self):
		same_sale_line_item = SaleLineItem(1, 2, 4.99, "037466022680")
		different_sale_line_item_1 = SaleLineItem(1, 2, 4.99, "629070500083")
		different_sale_line_item_2 = SaleLineItem(1, 3, 4.99, "037466022680")
		different_sale_line_item_3 = SaleLineItem(1, 2, 4.50, "037466022680")
		self.assertEqual("1; 2; 4.99; 037466022680", str(same_sale_line_item))
		self.assertEqual(str(self.sale_line_item.code) + "; " + str(self.sale_line_item.quantity) + "; " \
				   + str(self.sale_line_item.price) + "; " + self.sale_line_item.upc, str(same_sale_line_item))
		self.assertEqual(str(different_sale_line_item_1.code) + "; " + str(different_sale_line_item_1.quantity) + "; " \
				   + str(different_sale_line_item_1.price) + "; " + different_sale_line_item_1.upc, str(different_sale_line_item_1))
		self.assertEqual(str(different_sale_line_item_2.code) + "; " + str(different_sale_line_item_2.quantity) + "; " \
				   + str(different_sale_line_item_2.price) + "; " + different_sale_line_item_2.upc, str(different_sale_line_item_2))
		self.assertEqual(str(different_sale_line_item_3.code) + "; " + str(different_sale_line_item_3.quantity) + "; " \
				   + str(different_sale_line_item_3.price) + "; " + different_sale_line_item_3.upc, str(different_sale_line_item_3))
		self.assertEqual(str(same_sale_line_item), str(self.sale_line_item))
		self.assertNotEqual(str(different_sale_line_item_1), str(self.sale_line_item))
		self.assertNotEqual(str(different_sale_line_item_2), str(self.sale_line_item))
		self.assertNotEqual(str(different_sale_line_item_3), str(self.sale_line_item))

	def test_repr(self):
		same_sale_line_item = SaleLineItem(1, 2, 4.99, "037466022680")
		different_sale_line_item_1 = SaleLineItem(1, 2, 4.99, "629070500083")
		different_sale_line_item_2 = SaleLineItem(1, 3, 4.99, "037466022680")
		different_sale_line_item_3 = SaleLineItem(1, 2, 4.50, "037466022680")
		self.assertEqual("SaleLineItem(1, 2, 4.99, '037466022680')", repr(same_sale_line_item))
		self.assertEqual("SaleLineItem(" + repr(same_sale_line_item.code) + ", " + repr(same_sale_line_item.quantity) + ", " \
				   + repr(same_sale_line_item.price) + ", " + repr(same_sale_line_item.upc) + ")", repr(same_sale_line_item))
		self.assertEqual("SaleLineItem(" + repr(different_sale_line_item_1.code) + ", " + repr(different_sale_line_item_1.quantity) + ", " \
				   + repr(different_sale_line_item_1.price) + ", " + repr(different_sale_line_item_1.upc) + ")", repr(different_sale_line_item_1))
		self.assertEqual("SaleLineItem(" + repr(different_sale_line_item_2.code) + ", " + repr(different_sale_line_item_2.quantity) + ", " \
				   + repr(different_sale_line_item_2.price) + ", " + repr(different_sale_line_item_2.upc) + ")", repr(different_sale_line_item_2))
		self.assertEqual("SaleLineItem(" + repr(different_sale_line_item_3.code) + ", " + repr(different_sale_line_item_3.quantity) + ", " \
				   + repr(different_sale_line_item_3.price) + ", " + repr(different_sale_line_item_3.upc) + ")", repr(different_sale_line_item_3))
		self.assertEqual(repr(same_sale_line_item), repr(self.sale_line_item))
		self.assertNotEqual(repr(different_sale_line_item_1), repr(self.sale_line_item))
		self.assertNotEqual(repr(different_sale_line_item_2), repr(self.sale_line_item))
		self.assertNotEqual(repr(different_sale_line_item_3), repr(self.sale_line_item))

if __name__ == '__main__':
	unittest.main()