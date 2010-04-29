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
    
    def test_spool_content_creation(self):
        self.setUp()
        
        number = "03315509256"
        voicefile = "helloworld"
        salutation_file = "salutation"
        self.vc.asterisk_datacard = True 
        output_should = """
Channel: Datacard/datacard0/03315509256
MaxRetries: 3
RetryTime: 20
WaitTime: 30
Context: call-file-beispiel
Extension: s
Priority: 1
Set: PassedInfo=helloworld
Set: Salutation=salutation
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
        
    def test_conduct_call(self):
        #TODO: find some way to test the file-copy procedure
        pass

    def test_replace_special_characters(self):
        self.assertEquals(self.vc.replace_special_characters("T\xffst"), "T_st")
        self.assertEquals(self.vc.replace_special_characters("Test"), "Test")
        self.assertNotEquals(self.vc.replace_special_characters("T\xffst"), "T\xffst")
