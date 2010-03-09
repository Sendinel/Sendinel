try:
    import serial
except ImportError:
    print "Warning: SMS serial test not running since pyserial is" + \
            " not installed"

from time import sleep

from sendinel import settings
from sendinel.backend import smspdu


class SerialConnectionError(Exception):
    """
    This error should be raised if the handy sends an error
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


def get_serial():
    """
    open a serial connection
    """
    return serial.Serial(settings.SERIALPORTSMS)

def send_sms(recipient, message, ser_conn=None):
    """
    Send a SMS to the recipient with the Seria Port defined in the settings.py
    @param recipient: The telephone number like "018562358260
    @type recipient: A String
    @param message: The content for sending
    @type message: A string
    @param ser_conn: If the serial port from settings.py is not needed
    @type ser_conn: A Serial
    @raise SerialConnectionError: If a handy sends an error
    """
    ser = ser_conn
    
    if ser == None:
        ser = get_serial()
    if len(message)>160:
        message = message[0:160]
        
    """
    ser.write("AT+CMGF=1\r\n")
    ser.write("AT+CSMP?\r\n")
    serstring = 'AT+CMGS="' + recipient + '"\r\n'
    ser.write(serstring)
    ser.write(message)
    ser.write(chr(26))
    """
    
    # TODO remove this
    #print ser.portstr       # check which port was really used
    ser.setTimeout(0.2)
    
    def send(s):
        ser.write(s)
        sleep(0.2)
        while True:
            data = ser.read(64)
            if len(data) != 0:
                if str(data).lower().find("error") != -1:
                    raise SerialConnectionError(data)
            else:
                break
            
    send('AT\r')
    send('AT+CMGF=0\r')
    send('AT+CSMS=0\r')
    
    pdu = smspdu.PDU()
    message_pdu = pdu.encodeSMS(recipient, message)
    send('AT+CMGS=%i\r'%((len(message_pdu)-2)/2))
    send(message_pdu) 
    send(chr(26)) # CTRL+Z           
    ser.close()
