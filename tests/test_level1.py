import unittest
from calculator import Calculator

class TestOperations(unittest.TestCase):

# ARRANGE, ACT AND ASSSERT

    def setUp(self):
        self.calc = Calculator(8,2)

    def test_sum(self):
        self.assertEqual(self.calc.get_sum(), 10, "The sum function is incorrect")

    def test_minus(self):
        self.assertEqual(self.calc.get_minus(), 6, "The minus function is incorrect")

    def test_division(self):
        self.assertEqual(self.calc.get_division(), 4, "The division function is incorrect")

    def test_product(self):
        self.assertEqual(self.calc.get_product(), 16, "The product function is incorrect")

    def tearDown(self):
        return super().tearDown()

if __name__ == "__main__":
    unittest.main()

