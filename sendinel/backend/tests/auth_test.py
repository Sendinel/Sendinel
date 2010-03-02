import unittest
from sendinel.backend.authhelper import *
from sendinel.backend.models import AuthenticationCall
from sendinel.asterisk import log_call

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
        
        self.ah.log_path = "fake_file_log"
        
        number = "01621785295"
        number2 = "004916217852567"
        number3 = "016217852567"
        
        self.assertTrue(self.ah.authenticate(number, "Test"))
        self.assertTrue(self.ah.authenticate(number2, "Test 2"))
        
        fake = open("fake_file_log", 'w')
        fake.write("1265799666\t02/10/2010-12:01:06\t" + number + "\t2428534\n")
        fake.write("1265799667\t02/10/2010-12:01:07\t" + number3 + "\t2428534\n")
        
        fake.close()
        
        self.assertTrue(self.ah.check_log(number))
        self.assertTrue(self.ah.check_log(number2))
        
        
        number = "noValidNumber"
        self.assertFalse(self.ah.authenticate(number, "Test"))
        
    def test_check_log(self):

        self.ah.log_path="fake_file_log"
        
        self.ah.observe_number("0123456", "Test")
        self.ah.observe_number("0678945", "Test")
        
        fake = open("fake_file_log", 'w')
        fake.write("1265799666\t02/10/2010-12:01:06\t0654357987\t2428534\n")
        fake.write("1265799669\t02/10/2010-12:01:09\t0123456\t2428534\n")
        fake.close()
        
        self.assertTrue(self.ah.check_log("0123456"))
        self.assertFalse(self.ah.check_log("0678945"))
        
        self.assertRaises(NotObservedNumberException, self.ah.check_log, "01234")
        
    def test_observe_number(self):
        
        self.ah.clean_up_to_check()
        self.assertEquals(len(self.ah.to_check), 0)
        number = "0123456"
        self.ah.observe_number(number, "Test")
        self.ah.observe_number(number, "Test")
        self.assertEquals(len(self.ah.to_check), 1)
        
        
    def test_parse_log(self):
        
        self.ah.clean_up_to_check()
        self.ah.observe_number("012345678", "Test")
        self.ah.observe_number("087654321", "Test")
        
        fake = open("fake_file_log", 'w')
        fake.write("1265799669\t02/10/2010-12:01:09\t012345678\t2428534\n")
        fake.close()
        self.ah.parse_log("fake_file_log")
        
        self.assertTrue(self.ah.to_check["2345678"]["has_called"])
        self.assertFalse(self.ah.to_check["7654321"]["has_called"])
         
    def test_delete_old_numbers(self):

        self.ah.clean_up_to_check()
        self.ah.to_check["0123456"] = {"has_called":"False", "time":(time()-200)}
        self.ah.delete_old_numbers()
        self.assertEquals(len(self.ah.to_check), 0)
        
    def test_asterisk_log_call(self):
        class MockFile:
            def readlines(input):
                fake_data = """agi_request: call_log.agi
agi_channel: SIP/ext-sip-account-b50d4dc8
agi_language: en
agi_type: SIP
agi_uniqueid: 1267543275.24
agi_version: 1.6.2.0~rc2-0ubuntu1.2
agi_callerid: 01601234567
agi_calleridname: 01601234567
agi_callingpres: 0
agi_callingani2: 0
agi_callington: 0
agi_callingtns: 0
agi_dnid: 2428534
agi_rdnis: unknown
agi_context: von-voip-provider
agi_extension: 2428534
agi_priority: 1
agi_enhanced: 0.0
agi_accountcode: 
agi_threadid: -1258067088
"""
                return fake_data.splitlines()


        real_stdin = log_call.sys.stdin
        fake_stdin = MockFile()
        log_call.sys.stdin = fake_stdin
        
        AuthenticationCall.objects.all().delete()
        
        log_call.log_call()
        
        count = AuthenticationCall.objects.all().count()
        self.assertEquals(count, 1, "AuthenticationCall object was not created.")
        
        call = AuthenticationCall.objects.all()[0]
        self.assertEquals(call.number, "01601234567")

        log_call.sys.stdin = real_stdin
    