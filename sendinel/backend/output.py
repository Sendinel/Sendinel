import sms
import bluetooth
import voicecall

class OutputData(object):
    """
    Define an interface for OutputData.
    """
    class Meta:
        abstract = True
    
    data = None
    def __str__(self):
        return str(self.data)
        
    def send(self):
        raise NotImplementedError("send() needs to be overridden.")

class BluetoothOutputData(OutputData):
    """
    Define necessary OutputData for sending via bluetooth.
    """
    mac = None
    addressServer = None
    
    def send(self):
        bluetooth.send_vcal(self.addressServer, self.mac, self.data)

class SMSOutputData(OutputData):
    """
    Define necessary OutputData for sending via sms.
    """
    phone_number = None
    
    def send(self):
        sms.send_sms(self.phone_number, self.data)

class VoiceOutputData(OutputData):
    """
    Define necessary OutputData for sending via voice.
    """
    phone_number = None
    
    def send(self):
        pass
    
    

"""
Do the sending for the given outputData
@param  the outputData Object to send
"""

#TODO remove!
def send(outputData):
    outputData.send()

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

