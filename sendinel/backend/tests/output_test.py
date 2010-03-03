from django.test import TestCase
from sendinel.backend.output import *

class OutputTest(TestCase):
    """
    """
    def setUp(self):
        pass
        
    def test_implementation_of_send(self):
        outputData = OutputData()
        self.assertRaises(NotImplementedError, outputData.send)
    
    def test_send_smsoutputobject(self):
        message = "test"
        number = "1234"
    
        smsoutput = SMSOutputData()
        smsoutput.data = message
        smsoutput.phone_number = number
        
        def send_sms1(recipient, message2):
            self.assertEquals(message2, message)
            self.assertEquals(recipient, number)
            
        send_sms_old = sms.send_sms
        sms.send_sms = send_sms1
        #TODO send(smsoutput) is deprecated
        send(smsoutput)
        smsoutput.send()
        sms.send_sms = send_sms_old
        
    def test_send_bluetoothoutputobject(self):
        data = "test"
        mac = "1234"
        addressServer = "127"
    
        bluetoothoutput = BluetoothOutputData()
        bluetoothoutput.data = data
        bluetoothoutput.mac = mac
        bluetoothoutput.addressServer = addressServer
        
        def send_vcal1(addressServer2, mac2, data2):
            self.assertEquals(addressServer2, addressServer)
            self.assertEquals(mac2, mac)
            self.assertEquals(data2, data)
              
        send_vcal_old = bluetooth.send_vcal
        bluetooth.send_vcal = send_vcal1
        #TODO send(bluetoothoutput) is deprecated
        send(bluetoothoutput)
        bluetoothoutput.send()
        bluetooth.send_vcal = send_vcal_old

   def test_send_voiceoutputobject(self):
        self.phone_number = "test"
        self.data = "1234"
        d = sendinel.backend.output.VoiceOutputData()
        d.phone_number = self.phone_number
        d.data = self.data
        
        
        def conduct_call1(self, number, text, context):
            OutputTest.numberResult = number
            OutputTest.textResult = text
            

              
        self.conduct_call_old = sendinel.backend.output.voicecall.Voicecall.conduct_call
        
        sendinel.backend.output.voicecall.Voicecall.conduct_call = conduct_call1
        sendinel.backend.output.send(d)
        self.assertEquals(OutputTest.numberResult,self.phone_number)
        self.assertEquals(OutputTest.textResult,self.data)
        sendinel.backend.output.voicecall.Voicecall.conduct_call = self.conduct_call_old

