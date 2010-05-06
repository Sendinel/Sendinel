from string import Template

from django.db import models

from sendinel.backend import texthelper
from sendinel.backend.models import Patient, Sendable
from sendinel.backend.output import SMSOutputData, \
                                    VoiceOutputData


class InfoService(models.Model):
    """
    Represent a user group
    """
    
    members = models.ManyToManyField(Patient, through="Subscription")
    name = models.CharField(max_length=255,
                            unique=True,
                            blank=False,
                            null=False)

    def __unicode__(self):
        return self.name


class InfoMessage(Sendable):
    """
    Define a InfoMessage.
    """

    template = Template("$text")
    text = models.TextField()
    
    def __unicode__(self):
        return "InfoMessage to %s: '%s' via %s" % \
                                        (self.recipient.phone_number,
                                         self.text,
                                         self.way_of_communication)
    
    def get_data_for_sms(self):
        """
        Prepare OutputData for sms.
        Generate the message for an InfoMessage.
        Return SMSOutputData for sending.
        """
        
        data = SMSOutputData()           
        data.data = texthelper.generate_text({'text': self.text},
                                             InfoMessage.template)
        data.phone_number = self.recipient.phone_number
                
        return data
        
    def get_data_for_voice(self):
        """
        Prepare OutputData for voicecall.
        Generate the message for an InfoMessage.
        Return VoiceOutputData for sending.
        """
        
        data = VoiceOutputData()
        data.data = self.text
        data.phone_number = self.recipient.phone_number
            
        return data


class Subscription(models.Model):
    """
    Represents a patient's subscription to an infoservice
    """

    patient = models.ForeignKey(Patient)
    infoservice = models.ForeignKey(InfoService)

    way_of_communication = models.CharField(max_length = 9,
                                choices=Sendable.WAYS_OF_COMMUNICATION)

    def __unicode__(self):
        return "%s %s" % (unicode(self.infoservice), \
                          unicode(self.patient.phone_number))
