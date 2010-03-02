import sms
import bluetooth

class OutputData(object):
    """
    Define an interface for OutputData.
    """
    data = None
    def __str__(self):
        return str(self.data)

class BluetoothOutputData(OutputData):
    """
    Define necessary OutputData for sending via bluetooth.
    """
    mac = None
    addressServer = None

class SMSOutputData(OutputData):
    """
    Define necessary OutputData for sending via sms.
    """
    phone_number = None

class VoiceOutputData(OutputData):
    """
    Define necessary OutputData for sending via voice.
    """
    phone_number = None
    
    

"""
Do the sending for the given outputData
@param  the outputData Object to send
"""
def send(outputData):
    typ = type(outputData).__name__
    if typ == 'SMSOutputData':
        send_smsdata(outputData)
        
    elif typ == 'VoiceOutputData':
        send_voicedata(outputData)
        
    elif typ == 'BluetoothOutputData':
        send_bluetoothdata(outputData)
    else:
        pass
    
"""
Send a sms
"""
def send_smsdata(smsOutputData):
    recipient = smsOutputData.phone_number
    message = smsOutputData.data
    sms.send_sms(recipient, message)

"""
Call a number with a specific voice
"""
def send_voicedata(voiceOutputData):
    pass

"""
Send data to a bluetoothDevice
"""
def send_bluetoothdata(bluetoothOutputData):
    mac = bluetoothOutputData.mac
    data = bluetoothOutputData.data
    addressServer = bluetoothOutputData.addressServer
    bluetooth.send_vcal(addressServer, mac, data)