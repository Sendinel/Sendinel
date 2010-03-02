import sms
import bluetooth
import voicecall

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
    
    
def send(outputData):
    """
        Do the sending for the given outputData
        
        @param  outputData: the outputData Object to send
        @type   outputData: OutputData
    """
    typ = type(outputData).__name__
    if typ == 'SMSOutputData':
        send_smsdata(outputData)
        
    elif typ == 'VoiceOutputData':
        send_voicedata(outputData)
        
    elif typ == 'BluetoothOutputData':
        send_bluetoothdata(outputData)
    else:
        pass
    
def send_smsdata(smsOutputData):
    """
        Send a sms
        
        @param  smsOutputData:  the data needed for sending the message
        @type   smsOutputData:  SMSOutputData    
    """
    recipient = smsOutputData.phone_number
    message = smsOutputData.data
    sms.send_sms(recipient, message)

def send_voicedata(voiceOutputData):
    """
        Call a number with a specific voice
        
        @param  voiceOutputData:    data for putting the call
        @type   voiceOutputData:    VoiceOutputData
    """
    phone_number = voiceOutputData.phone_number
    voicetext = voiceOutputData.data
    call = voicecall.Voicecall()
    call.conduct_call(phone_number, voicetext, "outbound-call")

def send_bluetoothdata(bluetoothOutputData):
    """
        Send data to a bluetoothDevice
    """
    mac = bluetoothOutputData.mac
    data = bluetoothOutputData.data
    addressServer = bluetoothOutputData.addressServer
    bluetooth.send_vcal(addressServer, mac, data)