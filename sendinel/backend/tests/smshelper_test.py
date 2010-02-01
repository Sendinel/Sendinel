import unittest
import sys, os
sys.path.insert(0, os.path.abspath('../../'))
from sendinel.backend.smshelper import *

class SmshelperTest(unittest.TestCase):
    def test_correct_sms_content(self):
        text = generate_appointment_sms("13.2.98, 3:39", "ms daily","hodpiel hospital", "mr joijj")
        should_text = "Dear mr joijj, please remember your appointment" + \
                " at the hodpiel hospital at 13.2.98, 3:39 with doctor ms daily"
        self.assertEquals(should_text,text)
        
    def test_not_too_long_sms_content(self):
        text = generate_appointment_sms("13.2.98, 3:39" , "abcdefghijklmnopqrstuvwxyzabcd","hodpiel hospital", "mr joijj")
        should_text = "Dear mr joijj, please remember your appointment" + \
                " at the hodpiel hospital at 13.2.98, 3:39 with doctor abcdefghijklmnopqrstuvwxyzabcd"
        self.assertTrue(len(text) <= 160)
        self.assertEquals(should_text, text)
        
    def test_too_long_sms_content(self):
        text = generate_appointment_sms("13.2.98, 3:39" , "abcdefghijklmnopqrstuvwxyzabcd","hodpielitzkicitziktidiiiiii hospital", "mr joijjliputututututututututu")
        should_text = "Dear mr joijjliputututututututut, please remember your appointment" + \
                " at the hodpielitzkicitziktidiiiiii at 13.2.98, 3:39 with doctor abcdefghijklmnopqrstuvwxyza"
        self.assertTrue(len(text) <= 160)
        self.assertEquals(should_text, text)
        
if __name__ == '__main__':
    unittest.main()