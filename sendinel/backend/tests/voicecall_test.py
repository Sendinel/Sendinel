import unittest

linux_available = False
try:
    import grp
    import os
    import pwd
    import shutil
   
    linux_available = True
    
except ImportError:
    print "Warning: Linux operating system is required to run the voicecall functionality"
    
import sendinel.backend.voicecall    
import sendinel.settings    

class VoicecallTest(unittest.TestCase):

    def setUp(self):
        self.vc = sendinel.backend.voicecall.Voicecall()

    def test_conduct_sms(self):

        input_text = "This is a sample text"
        self.return_text = "This text was returned"
        input_number = "012345"
        input_context = "context-test"
        self.content_to_be_returned = "dummy-content"
        self.mock_return = "i was called"

        temporary_filename = "tmp"

        self.mock_input_text = ""
        self.mock_input_text2 = ""
        self.mock_input_number = ""
        self.mock_input_context = ""
        self.mock_input_filename = ""
        self.mock_input_filename2 = ""
        self.mock_content = ""
        
        def mock_replace_special_characters(text):
            self.mock_input_text = text
            return self.return_text

        def mock_create_sms_spool_content(text, number):
            self.mock_input_text2 = text
            self.mock_input_number = number            
            return self.content_to_be_returned

        def mock_create_spool_file(filename, content):
            self.mock_input_filename = filename
            self.mock_content = content

        def mock_move_spool_file(filename):
            self.mock_input_filename2 = filename
            return self.mock_return

        create_spool_file_backup = self.vc.create_spool_file
        self.vc.create_spool_file = mock_create_spool_file

        move_spool_file_backup = self.vc.move_spool_file
        self.vc.move_spool_file = mock_move_spool_file

        create_sms_spool_content_backup = self.vc.create_sms_spool_content
        self.vc.create_sms_spool_content = mock_create_sms_spool_content        

        replace_special_characters_backup = self.vc.replace_special_characters
        self.vc.replace_special_characters = mock_replace_special_characters

        # run the whole thing

        self.assertEquals(\
            self.vc.conduct_sms(input_number, input_text, input_context),
            self.mock_return)

        # let's see if everything was called correctly
        self.assertEquals(input_text, self.mock_input_text)
        self.assertEquals(self.return_text, self.mock_input_text2)
        self.assertEquals(input_number, self.mock_input_number)
        self.assertEquals(self.mock_input_text2, self.return_text)
        self.assertEquals(self.mock_input_number, input_number)
        self.assertEquals(self.mock_content, self.content_to_be_returned)
        self.assertEquals(self.mock_input_filename, temporary_filename)
        self.assertEquals(self.mock_input_filename2, temporary_filename)

        # restore everything back to normal
        self.vc.move_spool_file = move_spool_file_backup
        self.vc.create_spool_file = create_spool_file_backup
        self.vc.replace_special_characters = replace_special_characters_backup
        self.vc.create_sms_spool_content = create_sms_spool_content_backup

    def test_conduct_call(self):

        input_text = "This is a sample text"
        self.return_text = "This text was returned"
        input_number = "012345"
        input_context = "context-test"
        self.content_to_be_returned = "dummy-content"
        self.mock_return = "i was called"
        self.mock_salutation_return = "Returned salutation"
        self.mock_voicefile_return = "Returned voicefile"
                

        temporary_filename = "tmp"

        self.counter = 0

        self.mock_voicefile = ""
        self.mock_salutation = ""

        self.mock_replace_text = ""
        self.mock_input_text = ""
        self.mock_input_text2 = ""
        self.mock_input_number = ""
        self.mock_input_context = ""
        self.mock_output_filename = ""
        self.mock_output_filename2 = ""
        self.mock_content = ""
        
        def mock_replace_special_characters(text):
            self.mock_replace_text = text
            return self.return_text

        def mock_create_voicefile(text):
            self.counter += 1
            if self.counter == 1:
                self.mock_salutation_text = text
                return self.mock_salutation_return
            else:
                self.mock_input_text = text
                return self.mock_voicefile_return

        def mock_create_spool_content(number,
                                    voicefile,
                                    salutation,
                                    asterisk_extension,
                                    asterisk_sip_account,
                                    context):
            self.mock_voicefile = voicefile
            self.mock_salutation = salutation
            self.mock_input_number = number            
            return self.content_to_be_returned

        def mock_create_spool_file(filename, content):
            self.mock_output_filename = filename
            self.mock_content = content

        def mock_move_spool_file(filename):
            self.mock_output_filename2 = filename
            return self.mock_return

        create_spool_file_backup = self.vc.create_spool_file
        self.vc.create_spool_file = mock_create_spool_file

        create_voicefile_backup = self.vc.create_voicefile
        self.vc.create_voicefile = mock_create_voicefile

        move_spool_file_backup = self.vc.move_spool_file
        self.vc.move_spool_file = mock_move_spool_file

        create_spool_content_backup = self.vc.create_spool_content
        self.vc.create_spool_content = mock_create_spool_content        

        replace_special_characters_backup = self.vc.replace_special_characters
        self.vc.replace_special_characters = mock_replace_special_characters

        # run the whole thing

        sendinel.backend.voicecall.LINUX_AVAILABLE = True

        self.assertEquals(\
            self.vc.conduct_call(input_number, input_text, input_context),
            self.mock_return)

        sendinel.backend.voicecall.LINUX_AVAILABLE = False
        self.assertFalse(\
            self.vc.conduct_call(input_number, input_text, input_context))

        # let's see if everything was called correctly
        self.assertEquals(input_text, self.mock_replace_text)
        self.assertEquals(self.mock_salutation_text, self.vc.salutation)
        self.assertEquals(self.return_text, self.mock_input_text)
        self.assertEquals(input_number, self.mock_input_number)
        self.assertEquals(self.mock_input_number, input_number)
        self.assertEquals(self.mock_content, self.content_to_be_returned)
        self.assertEquals(self.mock_output_filename, temporary_filename)
        self.assertEquals(self.mock_output_filename2, temporary_filename)
        self.assertEquals(self.counter, 2)

        self.assertEquals(self.mock_voicefile_return, self.mock_voicefile)
        self.assertEquals(self.mock_salutation_return, self.mock_salutation)

        # restore everything back to normal
        self.vc.move_spool_file = move_spool_file_backup
        self.vc.create_spool_file = create_spool_file_backup
        self.vc.replace_special_characters = replace_special_characters_backup
        self.vc.create_spool_content = create_spool_content_backup
        self.vc.create_voicefile = create_voicefile_backup


    def test_sms_spool_content_creation(self):
        text = "This is a test"
        number = "1234"  

        output = self.vc.create_sms_spool_content(text, number)

        output_should = """
Channel: Local/2000
WaitTime: 2
RetryTime: 5
MaxRetries: 8000
Context: outbound-sms
Extension: s
Set: SmsNumber=1234
Set: Text=This is a test
Archive: true
"""
        self.assertEquals(output, output_should)

    
    def test_spool_content_creation(self):
        self.setUp()
        
        number = "03315509256"
        voicefile = "helloworld"
        salutation_file = "salutation"
        self.vc.asterisk_datacard = True 
        output_should = """
Channel: Local/3000
MaxRetries: 20
RetryTime: 20
WaitTime: 30
Context: call-file-beispiel
Extension: s
Priority: 1
Set: Receipient=Datacard/datacard0/03315509256
Set: PassedInfo=helloworld
Set: Salutation=salutation
Archive: true
"""
        
        output = self.vc.create_spool_content(number, voicefile, salutation_file, "s", "datacard0", "call-file-beispiel")
        
        self.assertEquals(output, output_should)
        
    def test_create_spool_file(self):
        self.setUp()
        VoicecallTest.write_called = False
        VoicecallTest.sample_content = "Sample Content"
        
        def open2(filename, attributes):
            class MockFile:
                def write(self, input):
                    if input == VoicecallTest.sample_content:
                        VoicecallTest.write_called = True

                def close(self):
                    return True
                    
            return MockFile()
        
        #overwrite open method
        sendinel.backend.voicecall.open = open2
        
        self.vc.create_spool_file("filename", VoicecallTest.sample_content)
        self.assertTrue(VoicecallTest.write_called)
        
        #revert open method
        sendinel.backend.voicecall.open = open
        pass
        
    def test_replace_special_characters(self):
        self.assertEquals(self.vc.replace_special_characters("T\xffst"), "T_st")
        self.assertEquals(self.vc.replace_special_characters("Test"), "Test")
        self.assertNotEquals(self.vc.replace_special_characters("T\xffst"), "T\xffst")
