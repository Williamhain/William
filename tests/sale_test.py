# sale_test.py
import unittest
from datetime import date
from pos.sale import Sale

class SaleTest(unittest.TestCase):

    def test_eq(self):
        # initialize test objects
        sale1 = Sale(1, date(2026, 2, 20), 9.98, 0.49, 0.69, 11.16)
        sale1a = Sale(1, date(2026, 2, 20), 9.98, 0.49, 0.69, 11.16)
        sale2 = Sale(2, date(2026, 2, 20), 18.99, 0.94, 1.32, 21.25)

        # test equality assertions
        self.assertIsNotNone(sale1, "initializing sale 1")
        self.assertEqual(sale1, sale1a, "same sales")
        self.assertNotEqual(sale1, sale2, "different sales")

    def test_string_representation(self):
        # verify valid string returns for simple representations
        sale1 = Sale(1, date(2026, 2, 20), 9.98, 0.49, 0.69, 11.16)
        self.assertIsInstance(str(sale1), str, "__str__ should return a string")
        self.assertIsInstance(repr(sale1), str, "__repr__ should return a string")

if __name__ == '__main__':
    unittest.main()