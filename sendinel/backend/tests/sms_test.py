import unittest

serial_available = False
try:
    import serial
    from backend.sms import *
    serial_available = True
except ImportError:
    print "Warning: SMS serial test not running since pyserial is" + \
            " not installed"

from backend.smspdu import *

if serial_available:
    class SMSTest(unittest.TestCase):
        """
        """
        def setUp(self):
            self.ser = serial.serial_for_url('loop://')

        
        def test_send_sms_commands_pdu_and_correct_len(self):
            """
            test the serial connection for sms pdu
            """
            recipient = '012345'
            message = 'this is the message\n via our serial connection\n' + \
                      ' we just want to test the behaviour\n becuase' + \
                      ' often it works wrong, but our app is pretty ' + \
                      'cool, but for correctness we test all methods'
            pdu = PDU()
            pdu_string =  pdu.encodeSMS(recipient,message[0:160])
        
            self.counter = 0
            self.commands = ['AT\r',
                'AT+CMGF=0\r',
                'AT+CSMS=0\r',
                'AT+CMGS=%i\r'%((len(pdu_string)-2)/2),
                pdu_string, 
                chr(26)]        
            def write(command):
                self.ser.write1(command)
                self.assertEquals(self.commands[self.counter],
                    self.ser.read(len(self.commands[self.counter])))
                self.counter += 1
            self.ser.close1 = self.ser.close
            self.ser.close = lambda: None

            self.ser.write1= self.ser.write
            self.ser.write = write
        
            send_sms(recipient, message, self.ser)
        
            self.ser.close = self.ser.close1
            self.ser.close()
        
