from sendinel.backend import sms, bluetooth, voicecall
from sendinel.logger import logger

class OutputData(object):
    """
    Define an interface for OutputData.
    """
    
    class Meta:
        abstract = True
    
    data = None
    def __str__(self):
        return unicode(self.data)
        
    def send(self):
        raise NotImplementedError("send() needs to be overridden.")

class BluetoothOutputData(OutputData):
    """
    Define necessary OutputData for sending via bluetooth.
    """
    
    bluetooth_mac_address = None
    server_address = None
    
    def send(self):
        logger.info("Sending via Bluetooth")
        return bluetooth.send_vcal(self.server_address, 
                            self.bluetooth_mac_address,
                            self.data)

class SMSOutputData(OutputData):
    """
    Define necessary OutputData for sending via sms.
    """
    
    phone_number = None
    
    def send(self):
        logger.info("Sending via SMS")
        sms.send_sms(self.phone_number, self.data)

class VoiceOutputData(OutputData):
    """
    Define necessary OutputData for sending via voice.
    """
    
    phone_number = None
    
    def send(self):
        logger.info("Sending via Phone Call")
        call = voicecall.Voicecall()
        call.conduct_call(self.phone_number, self.data, "outbound-call")
