import unittest
from sendinel.backend.authhelper import *

class AuthTest(unittest.TestCase):
    def test_number_formating(self):
        number = "+0123456789"
        self.assertEquals(format_number(number), "0123456789")
        number = "+01234/56789"
        self.assertEquals(format_number(number), "0123456789")
        number = "+01234 56789"
        self.assertEquals(format_number(number), "0123456789")
        number = "+0 1234 56789"
        self.assertEquals(format_number(number), "0123456789")        
        number = "+01234-56789"
        self.assertEquals(format_number(number), "0123456789")
        number = "abc"
        self.assertRaises(ValueError, format_number, number)
        number = "0123a45678"
        self.assertRaises(ValueError, format_number, number)        
        
    def test_is_number(self):
        number = "123"
        self.assertTrue(is_number(number))
        number = "abc"
        self.assertRaises(ValueError, is_number, number)
        number = "12 3"
        self.assertRaises(ValueError, is_number, number)

    def test_authenticate(self):
        number = "01621785295"
        self.assertTrue(authenticate(number))
        number = "noValidNumber"
        self.assertFalse(authenticate(number))