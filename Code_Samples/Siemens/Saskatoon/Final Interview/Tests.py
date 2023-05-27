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
    
    def test_remove_char(self):
        self.assertEqual(remove_char(123,3), "12")
        self.assertEqual(remove_char(111111,1), "")
        self.assertEqual(remove_char("ABCDDD",'D'), "ABC")
        with self.assertRaises(TypeError):
            remove_char()
        with self.assertRaises(TypeError):
            remove_char("1234")

    def test_count_char(self):
        self.assertEqual(count_char(123,3), 1)
        self.assertEqual(count_char(111111,1), 6)
        self.assertEqual(count_char("ABCDDD",'D'), 3)
        with self.assertRaises(TypeError):
            count_char()
        with self.assertRaises(TypeError):
            count_char("1234")

    def test_check_Palindrome(self):
        self.assertTrue(check_Palindrome(12321))
        self.assertFalse(check_Palindrome(1621))
        self.assertTrue(check_Palindrome("ABCBA"))
        self.assertFalse(check_Palindrome([]))
        with self.assertRaises(TypeError):
            check_Palindrome()

    def test_find_min_list(self):
        self.assertEqual(find_min_list([1,2,3]), 1)
        self.assertEqual(find_min_list([1,1,1,1,1,1]), 1)
        self.assertEqual(find_min_list([123]), 123)
        self.assertIsNone(find_min_list([]))
        with self.assertRaises(TypeError):
            find_min_list()
        with self.assertRaises(TypeError):
            find_min_list("aaaa")

    def test_divide(self):
        self.assertEqual(divide(10, 2), 5.0)
        self.assertEqual(divide(-10, 2), -5.0)
        self.assertEqual(divide(10, -2), -5.0)
        with self.assertRaises(AssertionError) as context:
            divide(10, 0)
        self.assertEqual(str(context.exception), "Cannot divide by zero.")

    def test_check_email(self):
        self.assertEqual(check_email("mo@gMail.com"), "Google Mail")
        self.assertEqual(check_email("0@yahoO.com"), "Yahoo mail")
        self.assertEqual(check_email("mo123123@rahnama.uk"), "Custom mail: rahnama.uk")
        with self.assertRaises(TypeError):
            check_email()


if __name__ == "__main__":
    unittest.main()