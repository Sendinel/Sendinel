import unittest
import sendinel.backend.voicecall

class VoicecallTest(unittest.TestCase):
    def setUp(self):
        self.vc = sendinel.backend.voicecall.Voicecall()
    
    def test_spool_content_creation(self):
        self.setUp()
        
        number = "03315509256"
        voicefile = "helloworld"
        
        output_should = """
Channel: SIP/03315509256@ext-sip-account
MaxRetries: 3
RetryTime: 20
WaitTime: 10
Context: call-file-beispiel
Extension: s
Priority: 1
Set: PassedInfo=helloworld
"""
        
        output = self.vc.create_spool_content(number, voicefile, "s", "ext-sip-account", "call-file-beispiel")
        
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
        