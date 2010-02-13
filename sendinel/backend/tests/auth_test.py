import unittest
from sendinel.backend.authhelper import *

class AuthTest(unittest.TestCase):
    def setUp(self):
        self.ah = AuthHelper()

    def test_number_formating(self):
        number = "0123456789"
        self.assertEquals(format_phone_number(number), "0123456789")             
        number = "+0123456789"
        self.assertEquals(format_phone_number(number), "0123456789")
        number = "+01234/56789"
        self.assertEquals(format_phone_number(number), "0123456789")
        number = "+01234 56789"
        self.assertEquals(format_phone_number(number), "0123456789")
        number = "+0 1234 56789"
        self.assertEquals(format_phone_number(number), "0123456789")        
        number = "+01234-56789"
        self.assertEquals(format_phone_number(number), "0123456789")
        number = "abc"
        self.assertRaises(ValueError, format_phone_number, number)
        number = "0123a45678"
        self.assertRaises(ValueError, format_phone_number, number)
        number = "+49123456789"
        self.assertRaises(ValueError, format_phone_number, number)          

    def test_authenticate(self):
        number = "01621785295"
        self.assertTrue(self.ah.authenticate(number))
        number = "noValidNumber"
        self.assertFalse(self.ah.authenticate(number))
        
    def test_check_log(self):
        self.ah.log_path="fake_file_log"
        
        self.ah.observe_number("0123456")
        self.ah.observe_number("0678945")
        
        fake = open("fake_file_log", 'w')
        fake.write("""1265799666\t02/10/2010-12:01:06\t0654357987\t2428534\n""")
        fake.write("""1265799669\t02/10/2010-12:01:09\t0123456\t2428534""")
        fake.close()
        
        self.assertTrue(self.ah.check_log("0123456"))
        self.assertFalse(self.ah.check_log("0678945"))
        
        self.assertRaises(NotObservedNumberException, self.ah.check_log, "01234")
        
    def test_observe_number(self):
        self.ah.clean_up_to_check()
        self.assertEquals(len(self.ah.to_check), 0)
        number = "0123456"
        self.ah.observe_number(number)
        self.ah.observe_number(number)
        self.assertEquals(len(self.ah.to_check), 1)
        
        
    def test_parse_log(self):
        self.ah.clean_up_to_check()
        self.ah.observe_number("012345678")
        self.ah.observe_number("087654321")
        
        fake = open("fake_file_log", 'w')
        fake.write("1265799669\t02/10/2010-12:01:09\t012345678\t2428534")
        fake.close()
        self.ah.parse_log("fake_file_log")
        
        self.assertTrue(self.ah.to_check["012345678"]["has_called"])
        self.assertFalse(self.ah.to_check["087654321"]["has_called"])
         
    def test_delete_old_numbers(self):
        self.ah.clean_up_to_check()
        self.ah.to_check["0123456"] = {"has_called":"False", "time":(time()-200)}
        self.ah.delete_old_numbers()
        self.assertEquals(len(self.ah.to_check), 0)