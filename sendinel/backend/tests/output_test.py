import unittest
import sendinel.backend.output

class OutputTest(unittest.TestCase):
    """
    """
    def setUp(self):
        pass
    
    def test_send_smsoutputobject(self):
        self.message = "test"
        self.number = "1234"
    
        d = sendinel.backend.output.SMSOutputData()
        d.data = self.message
        d.phone_number = self.number
        
        def send_sms1(recipient, message, ser_conn=None):
            self.assertEquals(message,self.message)
            self.assertEquals(recipient,self.number)
            
        self.send_sms_old = sendinel.backend.output.sms.send_sms
        sendinel.backend.output.sms.send_sms = send_sms1
        sendinel.backend.output.send(d)
        sendinel.backend.output.sms.send_sms = self.send_sms_old
        
    def test_send_bluetoothoutputobject(self):
        self.data = "test"
        self.mac = "1234"
        self.addressServer = "127"
    
        d = sendinel.backend.output.BluetoothOutputData()
        d.data = self.data
        d.mac = self.mac
        d.addressServer = self.addressServer
        
        def send_vcal1(addressServer, mac, data):
            self.assertEquals(addressServer,self.addressServer)
            self.assertEquals(mac,self.mac)
            self.assertEquals(data,self.data)
              
        self.send_vcal_old = sendinel.backend.output.bluetooth.send_vcal
        sendinel.backend.output.bluetooth.send_vcal = send_vcal1
        sendinel.backend.output.send(d)
        sendinel.backend.output.bluetooth.send_vcal = self.send_vcal_old

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