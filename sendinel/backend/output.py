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
    serverAddress = None
    
    def send(self):
        bluetooth.send_vcal(self.serverAddress, self.mac, self.data)

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
        call = voicecall.Voicecall()
        call.conduct_call(self.phone_number, self.data, "outbound-call")


