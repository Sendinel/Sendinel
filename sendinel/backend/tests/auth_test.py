import unittest
from sendinel.settings import COUNTRY_CODE_PHONE
from sendinel.backend import authhelper
from sendinel.backend.models import AuthenticationCall
from sendinel.asterisk import log_call

class AuthTest(unittest.TestCase):

    def test_number_formating(self):
        authhelper.COUNTRY_CODE_PHONE = "0027"
        authhelper.AREA_CODE_PHONE = "07"
        number = "+27723456789"
        self.assertEquals(authhelper.format_phonenumber(number), "0723456789")          
        number = "+277 234/567 89"
        self.assertEquals(authhelper.format_phonenumber(number), "0723456789")    
        number = "00277 234-56789"
        self.assertEquals(authhelper.format_phonenumber(number), "0723456789")
        number = "0123a45678"
        self.assertRaises(ValueError, authhelper.format_phonenumber, number)
        number = "0049123456789"
        self.assertRaises(ValueError, authhelper.format_phonenumber, number)
        number = "030123456789"
        self.assertRaises(ValueError, authhelper.format_phonenumber, number)          

        
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
        self.assertEquals(count, 1, "AuthenticationCall object wasn't created")
        
        call = AuthenticationCall.objects.all()[0]
        self.assertEquals(call.number, "01601234567")

        log_call.sys.stdin = real_stdin
    
    def test_check_and_delete_authentication_call(self):
        AuthenticationCall.objects.all().delete()
        AuthenticationCall(number = "01601234567").save()

        call_received = authhelper.check_and_delete_authentication_call(" 0160 1234567 ")
        self.assertTrue(call_received)
        call_received = authhelper.check_and_delete_authentication_call(" 0160 1234567 ")
        self.assertFalse(call_received)


