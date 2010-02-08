import unittest
import sys, os
sys.path.insert(0, os.path.abspath('../../'))
from sendinel.backend.smshelper import *
from string import Template

class SmshelperTest(unittest.TestCase):
    def test_generate_sms_appointment(self):
        text = generate_sms({'date': "13.2.98, 3:39", 'doctor': "ms daily", \
                            'hospital': "hodpiel hospital", 'name': "mr joijj"},\
                             Template("Dear $name, please remember your appointment" + \
                                " at the $hospital at $date with doctor $doctor"))  
        should_text = "Dear mr joijj, please remember your appointment" + \
                " at the hodpiel hospital at 13.2.98, 3:39 with doctor ms daily"
        self.assertEquals (text, should_text)
        self.assertTrue(len(text) <= 160)
        
    def test_generate_sms_message(self):
        text = generate_sms({'free_text':"Hello Mrs. Joirie, your medication is there. " \
                                + "Please remember to pay 2 $."}, Template("$free_text"))
        should_text = "Hello Mrs. Joirie, your medication is there. Please remember to pay 2 $."
        self.assertEquals (text, should_text)
        self.assertTrue(len(text) <= 160)
        
    def test_generate_appointment_sms_content(self):
        specific_content = {'date':"13.2.98, 3:39", 'doctor': "ms daily",\
           'hospital': "hodpiel hospital", 'name':"mr joijj"}
        sms_format = "Dear %s, please remember your appointment" + \
                " at the %s at %s with doctor %s"   
        text = generate_appointment_sms(specific_content, sms_format)
        should_text = "Dear mr joijj, please remember your appointment" + \
                " at the hodpiel hospital at 13.2.98, 3:39 with doctor ms daily"
        self.assertEquals(should_text,text)
        
    def test_generate_appointment_sms_length(self):
        specific_content = {'date':"13.2.98, 3:39" ,'doctor': "abcdefghijklmnopqrstuvwxyzabcd",
            'hospital':"hodpiel hospital", 'name':"mr joijj"}
        sms_format = "Dear %s, please remember your appointment" + \
            " at the %s at %s with doctor %s"   
        text = generate_appointment_sms(specific_content, sms_format)
        should_text = "Dear mr joijj, please remember your appointment" + \
                " at the hodpiel hospital at 13.2.98, 3:39 with doctor abcdefghijklmnopqrstuvwxyzabcd"
        self.assertTrue(len(text) <= 160)
        self.assertEquals(should_text, text)
        
    def test_generate_appointment_sms_cut_off(self):
        specific_content = {'date':"13.2.98, 3:39" ,\
                            'doctor':"abcdefghijklmnopqrstuvwxyzabcd",\
                            'hospital':"hodpielitzkicitziktidiiiiii hospital", \
                            'name':"mr joijjliputututututututututu"}
        sms_format = "Dear %s, please remember your appointment" + \
            " at the %s at %s with doctor %s"   
        text = generate_appointment_sms(specific_content, sms_format)
        should_text = "Dear mr joijjlipututututututut, please remember your"\
          + " appointment at the hodpielitzkicitziktidiiii at 13.2.98, "\
          + "3:39 with doctor abcdefghijklmnopqrstuvwxy"
        self.assertTrue(len(text) <= 160)
        self.assertEquals(should_text, text)
        
if __name__ == '__main__':
    unittest.main()