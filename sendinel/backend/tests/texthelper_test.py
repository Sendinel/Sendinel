from sendinel.backend import texthelper
import unittest
from string import Template


class TesthelperTest(unittest.TestCase):

    def setUp(self):
        self.salutation = texthelper.SMS_SALUTATION
        texthelper.SMS_SALUTATION = "Hello "
        
    def tearDown(self):
        super(TesthelperTest, self).tearDown()
        
        texthelper.SMS_SALUTATION = self.salutation

    def test_date_to_text(self): 
        date = texthelper.date_to_text(3, 18, 3, 11, 40)
        
        self.assertEquals(date["date"], 'Wednesday, eighteenth of March')
        self.assertEquals(date["time"], "eleven forty")
        
    def test_generate_text_appointment(self):
        text = texthelper.generate_text({'date': "13.2.98", 'time': "3:39", 'doctor': "ms daily-binnessy-dayteewart", \
                            'hospital': "hodpiel hospital at the " +\
                            "lake with the frog and the tree",\
                            'name': "mr jameson-bitterall-wertifial"},\
                             Template("$name, please remember your appointment" + \
                                " at the $hospital at $date, $time with doctor $doctor"))  
        should_text = texthelper.SMS_SALUTATION + "mr jameson-bitterall-wertif, please remember " +\
                        "your appointment at the hodpiel hospital at the " + \
                        "lak at 13.2.98, 3:39 with doctor ms daily-binnessy-dayteewar"
        self.assertTrue(len(text) <= 160)
        self.assertEquals (text, should_text)

    def test_generate_text_message(self):
        text = texthelper.generate_text({'free_text':"Mrs. Joirie, your medicine is there. " \
                                + "Please remember to pay 2 $."}, Template("$free_text"))
        should_text = texthelper.SMS_SALUTATION + "Mrs. Joirie, your medicine is there. Please remember to pay 2 $."
        self.assertEquals (text, should_text)
        self.assertTrue(len(text) <= 160)
        
    def test_generate_appointment_text_cut_off(self):
        text =  texthelper.generate_text({'text': "Hello my name is james I am 22 years old " + \
                             "and i really want to go to bali and make holidays " + \
                             "since my last holidays are ages ago and i think a " + \
                             "little bit less stress would be fun to have"}, \
                             Template ('What an interesting text :$text'))
        should_text = texthelper.SMS_SALUTATION + "What an interesting text :Hello my name is james I am 22 " + \
                        "years old and i really want to go to bali and make " + \
                        "holidays since my last holidays are ages ago a"
        self.assertTrue(len(text) <= 160)
        self.assertEquals(should_text, text)

    def test_generate_appointment_text_no_cut(self):
        text =  texthelper.generate_text({'text': "Hello my name is james I am 22 years old " + \
                             "and i really want to go to bali and make holidays " + \
                             "since my last holidays are ages ago and i think a " + \
                             "little bit less stress would be fun to have"}, \
                             Template ('What an interesting text :$text'), False)
        should_text = "What an interesting text :Hello my name is james I am 22 years old " + \
                             "and i really want to go to bali and make holidays " + \
                             "since my last holidays are ages ago and i think a " + \
                             "little bit less stress would be fun to have"
        self.assertTrue(len(text) >= 160)
        self.assertEquals(should_text, text)
        
    def test_generate_appointment_text_cut_off_special_fields(self):
        specific_content = {'date':"13.2.98, 3:39" ,\
                            'doctor':"abcdefghijklmnopqrstuvwxyzabcd",\
                            'hospital':"hodpielitzkicitziktidiiiiii hospital", \
                            'name':"mr joijjliputututututututututu"}
        text_template = Template("Dear $name, please remember your appointment" + \
            " at the $hospital at $date with doctor $doctor")   
        text = texthelper.generate_text(specific_content, text_template)
        should_text = texthelper.SMS_SALUTATION + "Dear mr joijjlipututututututut, please remember your " + \
                        "appointment at the hodpielitzkicitziktidiiii at " + \
                        "13.2.98, 3:39 with doctor abcdefghijklmnopqrstuvwxy"
        self.assertTrue(len(text) <= 160)
        self.assertEquals(should_text, text)
        