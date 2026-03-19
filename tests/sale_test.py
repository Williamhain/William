from unittest import TestCase
from unittest import main
from pos.sale import Sale
from pos.sale_line_item import SaleLineItem
from datetime import date, datetime

class SaleTest(TestCase):
	
	def setUp(self):
		self.sale = Sale(1111112000, date(2026, 2, 20), 9.98, 0.49, 0.69, 11.16)

	def test_eq(self):
		same_sale = Sale(1111112000, date(2026, 2, 20), 9.98, 0.49, 0.69, 11.16)
		different_sale_1 = Sale(1111112000, date(2026, 2, 21), 9.98, 0.49, 0.69, 11.16)
		different_sale_2 = Sale(1111114444, date(2026, 2, 20), 18.99, 0.94, 1.32, 21.25)
		different_sale_3 = Sale(1111112000, date(2026, 2, 20), 18.99, 0.94, 1.32, 21.25)
		self.assertTrue(self.sale == self.sale)
		self.assertTrue(self.sale == same_sale)
		self.assertFalse(self.sale == different_sale_1)
		self.assertFalse(self.sale == different_sale_2)
		self.assertFalse(self.sale == different_sale_3)

	def test_str(self):
		same_sale = Sale(1111112000, date(2026, 2, 20), 9.98, 0.49, 0.69, 11.16)
		different_sale_1 = Sale(1111112000, date(2026, 2, 21), 9.98, 0.49, 0.69, 11.16)
		different_sale_2 = Sale(1111114444, date(2026, 2, 20), 18.99, 0.94, 1.32, 21.25)
		different_sale_3 = Sale(1111112000, date(2026, 2, 20), 18.99, 0.94, 1.32, 21.25)
		self.assertEqual("1111112000; 2026-02-20; 9.98; 0.49; 0.69; 11.16", str(self.sale))
		self.assertEqual("1111112000; 2026-02-20; 9.98; 0.49; 0.69; 11.16", str(same_sale))
		self.assertEqual("1111112000; 2026-02-21; 9.98; 0.49; 0.69; 11.16", str(different_sale_1))
		self.assertEqual("1111114444; 2026-02-20; 18.99; 0.94; 1.32; 21.25", str(different_sale_2))
		self.assertEqual("1111112000; 2026-02-20; 18.99; 0.94; 1.32; 21.25", str(different_sale_3))
		self.assertEqual(str(same_sale), str(self.sale))
		self.assertNotEqual(str(different_sale_1), str(self.sale))
		self.assertNotEqual(str(different_sale_2), str(self.sale))
		self.assertNotEqual(str(different_sale_3), str(self.sale))

	def test_repr(self):
		same_sale = Sale(1111112000, date(2026, 2, 20), 9.98, 0.49, 0.69, 11.16)
		different_sale_1 = Sale(1111112000, date(2026, 2, 21), 9.98, 0.49, 0.69, 11.16)
		different_sale_2 = Sale(1111114444, date(2026, 2, 20), 18.99, 0.94, 1.32, 21.25)
		different_sale_3 = Sale(1111112000, date(2026, 2, 20), 18.99, 0.94, 1.32, 21.25)
		self.assertEqual("Sale(1111112000, datetime.date(2026, 2, 20), 9.98, 0.49, 0.69, 11.16)", repr(self.sale))
		self.assertEqual("Sale(1111112000, datetime.date(2026, 2, 20), 9.98, 0.49, 0.69, 11.16)", repr(same_sale))
		self.assertEqual("Sale(1111112000, datetime.date(2026, 2, 21), 9.98, 0.49, 0.69, 11.16)", repr(different_sale_1))
		self.assertEqual("Sale(1111114444, datetime.date(2026, 2, 20), 18.99, 0.94, 1.32, 21.25)", repr(different_sale_2))
		self.assertEqual("Sale(1111112000, datetime.date(2026, 2, 20), 18.99, 0.94, 1.32, 21.25)", repr(different_sale_3))
		self.assertEqual(repr(same_sale), repr(self.sale))
		self.assertNotEqual(repr(different_sale_1), repr(self.sale))
		self.assertNotEqual(repr(different_sale_2), repr(self.sale))
		self.assertNotEqual(repr(different_sale_3), repr(self.sale))

	def test_create_sale_line_item(self):
		# some sale line items that may be created
		expected_sale_line_item_1 = SaleLineItem(1, 2, 4.99, "037466022680")
		expected_sale_line_item_2 = SaleLineItem(2, 1, 18.99, "629070500083")
		expected_sale_line_item_3 = SaleLineItem(3, 1.5, 5.93, "000000003294")

		# add one sale line item
		actual_sale_line_item = self.sale.create_sale_line_item(2, 4.99, "037466022680")
		self.assertIsNotNone(actual_sale_line_item, "sale line item 1 was created and is valid")

		# implement __eq__(self, other) in Post to compare sale line items based on their code and text
		self.assertEqual(expected_sale_line_item_1, actual_sale_line_item, "sale line item 1 was created and its data are correct")

		# after creating the sale line item, one should be able to search it
		actual_sale_line_item = self.sale.search_sale_line_item(1)
		self.assertIsNotNone(actual_sale_line_item, "sale line item created and retrieved cannot be null")
		self.assertEqual(expected_sale_line_item_1, actual_sale_line_item, "sale line item 1 was created, retrieved and its data are correct")

		# add a second sale line item
		actual_sale_line_item = self.sale.create_sale_line_item( 1, 18.99, "629070500083")
		self.assertIsNotNone(actual_sale_line_item, "sale line item 2 was created and is valid")
		self.assertEqual(expected_sale_line_item_2, actual_sale_line_item, "sale line item 2 was created and its data are correct")

		# after creating the sale line item, one should be able to search it
		actual_sale_line_item = self.sale.search_sale_line_item(2)
		self.assertIsNotNone(actual_sale_line_item, "sale line item created and retrieved cannot be null")
		self.assertEqual(expected_sale_line_item_2, actual_sale_line_item, "sale line item 2 was created, retrieved and its data are correct")

		# add a third sale line item
		actual_sale_line_item = self.sale.create_sale_line_item(1.5, 5.93, "000000003294")
		self.assertIsNotNone(actual_sale_line_item, "sale line item 3 was created and is valid")
		self.assertEqual(expected_sale_line_item_3, actual_sale_line_item, "sale line item 3 was created and its data are correct")

		# after creating the sale line item, one should be able to search it
		actual_sale_line_item = self.sale.search_sale_line_item(3)
		self.assertIsNotNone(actual_sale_line_item, "sale line item created and retrieved cannot be null")
		self.assertEqual(expected_sale_line_item_3, actual_sale_line_item, "sale line item 3 was created, retrieved and its data are correct")

		# creating new sale line items should not affect previous sale line items
		actual_sale_line_item = self.sale.search_sale_line_item(2)
		self.assertIsNotNone(actual_sale_line_item, "sale line item created and retrieved cannot be null regardless of search order")
		self.assertEqual(expected_sale_line_item_2, actual_sale_line_item, "sale line item 2 was created, retrieved and its data are correct regardless of search order")
		actual_sale_line_item = self.sale.search_sale_line_item(1)
		self.assertIsNotNone(actual_sale_line_item, "sale line item created and retrieved cannot be null regardless of search order")
		self.assertEqual(expected_sale_line_item_1, actual_sale_line_item, "sale line item 1 was created, retrieved and its data are correct regardless of search order")


	def test_list_sale_line_items(self):
		# some sale line items that may be listed
		expected_sale_line_item_1 = SaleLineItem(1, 2, 4.99, "037466022680")
		expected_sale_line_item_2 = SaleLineItem(2, 1, 18.99, "629070500083")
		expected_sale_line_item_3 = SaleLineItem(3, 1.5, 5.93, "000000003294")
		expected_sale_line_item_4 = SaleLineItem(4, 3, 6.99, "661172000122")
		expected_sale_line_item_5 = SaleLineItem(5, 4, 5.49, "065684112241")

		# listing sale line items when the current patient has no sale line items
		sale_line_items_list = self.sale.list_sale_line_items()
		self.assertEqual(len(sale_line_items_list), 0, "list of sale line items for patient has size 0")

		# listing sale line items in a singleton list
		actual_sale_line_item = self.sale.create_sale_line_item(2, 4.99, "037466022680")
		sale_line_items_list = self.sale.list_sale_line_items()
		self.assertEqual(len(sale_line_items_list), 1, "list of sale line items for patient has size 1")
		self.assertEqual(sale_line_items_list[0], expected_sale_line_item_1, "first sale line item in the list is sale line item 1")

		# add some more sale line items
		actual_sale_line_item = self.sale.create_sale_line_item(1, 18.99, "629070500083")
		actual_sale_line_item = self.sale.create_sale_line_item(1.5, 5.93, "000000003294")
		actual_sale_line_item = self.sale.create_sale_line_item(3, 6.99, "661172000122")
		actual_sale_line_item = self.sale.create_sale_line_item(4, 5.49, "065684112241")

		# listing sale line items in a larger list
		sale_line_items_list = self.sale.list_sale_line_items()
		self.assertEqual(len(sale_line_items_list), 5, "list of sale line items has size 5")
		self.assertEqual(sale_line_items_list[0], expected_sale_line_item_1, "sale line item 5 is the first in the list of sale line items")
		self.assertEqual(sale_line_items_list[1], expected_sale_line_item_2, "sale line item 4 is the second in the list of sale line items")
		self.assertEqual(sale_line_items_list[2], expected_sale_line_item_3, "sale line item 3 is the third in the list of sale line items")
		self.assertEqual(sale_line_items_list[3], expected_sale_line_item_4, "sale line item 2 is the fourth in the list of sale line items")
		self.assertEqual(sale_line_items_list[4], expected_sale_line_item_5, "sale line item 1 is the fifth in the list of sale line items")


if __name__ == '__main__':
	unittest.main()