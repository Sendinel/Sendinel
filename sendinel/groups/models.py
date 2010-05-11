from string import Template

from django.db import models
from django.utils.translation import ugettext_lazy

from sendinel.backend import texthelper
from sendinel.backend.models import Patient, Sendable
from sendinel.backend.output import SMSOutputData, \
                                    VoiceOutputData


class InfoService(models.Model):
    """
    Represent a user group.
    Existing types are 'information' and 'medicine' 
    whereas information-groups send regular messages to their 
    subscribers, medicine deletes the group after sending a message
    """
    
    TYPES = (
        ('information', ugettext_lazy("Information Group")),
        ('medicine', ugettext_lazy('Waiting List for Medicine'))
    )
    TYPE_TEXTS = {
        'information': {
            'title': ugettext_lazy('Information Groups'),
            'name': ugettext_lazy('information group'),
            'members_button': ugettext_lazy('Group members'),
            'remove_button': ugettext_lazy('Remove group'),
            'form_field_description': ugettext_lazy('Inform patients about:'),
            'table_head': ugettext_lazy('Information')
        },
        'medicine': {
            'title': ugettext_lazy('Waiting Lists for Medicine'),
            'name': ugettext_lazy('waiting list for medicine'),
            'members_button': ugettext_lazy('List members'),
            'remove_button': ugettext_lazy('Remove list'),
            'form_field_description':
            ugettext_lazy('The patients are waiting for the following medicine:'),
            'table_head': ugettext_lazy('Medicine')
        },
    }
    
    
    members = models.ManyToManyField(Patient, through = "Subscription")
    name = models.CharField(max_length = 255,
                            default = None,
                            unique = True,
                            blank = False,
                            null = False)
    type = models.CharField(max_length = 255, 
                            choices = TYPES,
                            default = None,
                            blank = False, 
                            null = False)
                            
    def __unicode__(self):
        return self.name
    
    def member_count(self):
        return self.members.all().count()
    
    def texts(self):
        """
        Returns the text blocks associated with the group's type.
        """
        return self.TYPE_TEXTS[self.type]


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
