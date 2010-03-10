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
        smsoutput.send()
        sms.send_sms = send_sms_old
        
    def test_send_bluetoothoutputobject(self):
        data = "test"
        mac = "1234"
        server_address = "127"
    
        bluetoothoutput = BluetoothOutputData()
        bluetoothoutput.data = data
        bluetoothoutput.bluetooth_mac_address = mac
        bluetoothoutput.server_address = server_address
        
        def send_vcal1(server_address2, mac2, data2):
            self.assertEquals(server_address2, server_address)
            self.assertEquals(mac2, mac)
            self.assertEquals(data2, data)
              
        send_vcal_old = bluetooth.send_vcal
        bluetooth.send_vcal = send_vcal1
        bluetoothoutput.send()
        bluetooth.send_vcal = send_vcal_old

    def test_send_voiceoutputobject(self):
        phone_number = "1234"
        data = "test"
        voicecalldata = VoiceOutputData()
        voicecalldata.phone_number = phone_number
        voicecalldata.data = data
        
        def conduct_call1(self, number, text, context):
            #use class variables because of contextbinding to VoiceOutputData
            OutputTest.phone_number_value = number
            OutputTest.text_value = text
              
        conduct_call_old = voicecall.Voicecall.conduct_call
        voicecall.Voicecall.conduct_call = conduct_call1
        voicecalldata.send()
        voicecall.Voicecall.conduct_call = conduct_call_old
        
        self.assertEquals(self.text_value, data)
        self.assertEquals(self.phone_number_value, phone_number)

