# sale_line_item_test.py
import unittest
from pos.sale_line_item import SaleLineItem

class SaleLineItemTest(unittest.TestCase):
    def setUp(self):
        #create some sale line items as examples to use for multiple tests
        self.item1 = SaleLineItem(1, 2.0, 4.99, "037466022680")
        self.item2 = SaleLineItem(1, 2.0, 4.99, "037466022680")
        self.item3 = SaleLineItem(2, 1.0, 18.99, "629070500083")

    def test_initialization(self):
        #verify that the constructor assigns attributes properly
        self.assertEqual(self.item1.code, 1, "Code should match the initialized value")
        self.assertEqual(self.item1.quantity, 2.0, "Quantity should match")
        self.assertEqual(self.item1.price, 4.99, "Price should match")
        self.assertEqual(self.item1.upc, "037466022680", "UPC should match")

    def test_equality(self):
        #verify that two separate items with the same data are equal
        self.assertTrue(self.item1 == self.item2, "Items with identical data should be equal")
        
        #verify that items with different data are not equal
        self.assertFalse(self.item1 == self.item3, "Items with different data should not be equal")

    def test_string_representation(self):
        #verify that the string representations return valid strings
        self.assertIsInstance(str(self.item1), str, "__str__ should return a string")
        self.assertIsInstance(repr(self.item1), str, "__repr__ should return a string")

if __name__ == '__main__':
    unittest.main()