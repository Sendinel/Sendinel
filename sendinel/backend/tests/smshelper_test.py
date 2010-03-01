from sendinel.backend.smshelper import *
import unittest
from string import Template


class SmshelperTest(unittest.TestCase):
    def test_generate_sms_appointment(self):
        text = generate_sms({'date': "13.2.98, 3:39", 'doctor': "ms daily-binnessy-dayteewart", \
                            'hospital': "hodpiel hospital at the " +\
                            "lake with the frog and the tree",\
                            'name': "mr jameson-bitterall-wertifial"},\
                             Template("Dear $name, please remember your appointment" + \
                                " at the $hospital at $date with doctor $doctor"))  
        should_text = "Dear mr jameson-bitterall-wertif, please remember " +\
                        "your appointment at the hodpiel hospital at the " + \
                        "lak at 13.2.98, 3:39 with doctor ms daily-binnessy-dayteewar"
        self.assertTrue(len(text) <= 160)
        self.assertEquals (text, should_text)

    def test_generate_sms_message(self):
        text = generate_sms({'free_text':"Hello Mrs. Joirie, your medication is there. " \
                                + "Please remember to pay 2 $."}, Template("$free_text"))
        should_text = "Hello Mrs. Joirie, your medication is there. Please remember to pay 2 $."
        self.assertEquals (text, should_text)
        self.assertTrue(len(text) <= 160)
        
    def test_generate_appointment_sms_cut_off(self):
        text =  generate_sms({'text': "Hello my name is james I am 22 years old " + \
                             "and i really want to go to bali and make holidays " + \
                             "since my last holidays are ages ago and i think a " + \
                             "little bit less stress would be fun to have"}, \
                             Template ('What an interesting text :$text'))
        should_text = "What an interesting text :Hello my name is james I am 22 " + \
                        "years old and i really want to go to bali and make " + \
                        "holidays since my last holidays are ages ago and i t"
        self.assertTrue(len(text) <= 160)
        self.assertEquals(should_text, text)
        
    def test_generate_appointment_sms_cut_off_special_fields(self):
        specific_content = {'date':"13.2.98, 3:39" ,\
                            'doctor':"abcdefghijklmnopqrstuvwxyzabcd",\
                            'hospital':"hodpielitzkicitziktidiiiiii hospital", \
                            'name':"mr joijjliputututututututututu"}
        sms_template = Template("Dear $name, please remember your appointment" + \
            " at the $hospital at $date with doctor $doctor")   
        text = generate_sms(specific_content, sms_template)
        should_text = "Dear mr joijjliputututututututut, please remember your " + \
                        "appointment at the hodpielitzkicitziktidiiiiii at " + \
                        "13.2.98, 3:39 with doctor abcdefghijklmnopqrstuvwxyza"
        self.assertTrue(len(text) <= 160)
        self.assertEquals(should_text, text)
        