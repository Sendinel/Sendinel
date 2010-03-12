from time import sleep

from sendinel import settings

import sendinel.backend.voicecall

def send_sms(recipient, message, ser_conn=None):
    """
    Send a SMS to the recipient with the Seria Port defined in the settings.py
    @param recipient: The telephone number like "018562358260
    @type recipient: A String
    @param message: The content for sending
    @type message: A string
    """

    vc = sendinel.backend.voicecall.Voicecall()
    vc.conduct_sms(recipient, message, "outbound-sms")
