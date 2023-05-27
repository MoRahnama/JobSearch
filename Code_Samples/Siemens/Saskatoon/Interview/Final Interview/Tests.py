# Unit tests

import unittest
from Functions import *

class Test_Functins(unittest.TestCase):

    def test_reverse_integer(self):
        self.assertEqual(reverse_integer(123), 321)
        self.assertEqual(reverse_integer(10001), 10001)
        self.assertEqual(reverse_integer(1111), 1111)
        with self.assertRaises(TypeError):
            reverse_integer("aaaa")

    def test_count_digits(self):
        self.assertEqual(count_digits(123), 3)
        self.assertEqual(count_digits(111111), 6)
        with self.assertRaises(TypeError):
            count_digits()
        with self.assertRaises(TypeError):
            count_digits("aaaa")

if __name__ == "__main__":
    unittest.main()