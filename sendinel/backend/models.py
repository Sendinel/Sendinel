from datetime import datetime

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy

from sendinel.settings import DEFAULT_HOSPITAL_NAME, \
                              LANGUAGE_CODE
from sendinel.backend.output import SMSOutputData, \
                                    VoiceOutputData, \
                                    BluetoothOutputData
from sendinel.logger import logger

class User(models.Model):
    """
    Define an interface for a user of the system.
    """
    
    class Meta:
        abstract = True
    name = models.CharField(max_length=255, blank=True, null=True)
    
    def __unicode__(self):
        return self.name or "unnamed user"
    
class Patient(User):
    """
    Represent a patient.
    """
    
    phone_number = models.CharField(max_length = 20)
    
    def __unicode__(self):
        return "Patient <%s>" % self.phone_number

class Hospital(models.Model):
    """
    Represent a Hospital.
    """
    
    name = models.CharField(max_length = 255)
    current_hospital = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.name
    
    @classmethod
    def get_current_hospital(cls):
        """
        Return the standard current hospital
        """
        
        try:
            hospital = Hospital.objects.get(current_hospital = True)
        except Hospital.DoesNotExist:
            hospital = Hospital(name = DEFAULT_HOSPITAL_NAME, \
            current_hospital = True)
            hospital.save() 
        return hospital    
        

class WayOfCommunication(models.Model):
    """
    Represent a possible Way of Communication like SMS
    """
    
    name = models.CharField(max_length = 255, blank = False, null = False)
    verbose_name = models.CharField(max_length = 255)
    enabled = models.BooleanField()
    can_send_immediately = models.BooleanField()
    
    def __unicode__(self):
        return self.verbose_name
        
def get_enabled_wocs():
    """
    Return all Ways of Communication that are enabled
    """
    return WayOfCommunication.objects.filter(enabled = True)
    
def get_immediate_wocs():
    """
    Return all Ways of Communication that are enabled
    and can be send immediately
    """
    return WayOfCommunication.objects.filter(enabled = True, \
                                             can_send_immediately = True)                                                    

def get_woc(woc_name):
    """
    Return the WayOfCommunication-Object where the name equals the 
    given woc_name
    """
    return WayOfCommunication.objects.get(name = woc_name)        

def get_woc_by_id(woc_id):
    """
    Return the WayOfCommunication-Object where the name equals the 
    given woc_name
    """
    return WayOfCommunication.objects.get(pk = woc_id) 

class Sendable(models.Model):
    """
    Define an interface for a Sendable object.
    """

    class Meta:
        abstract = True
        
    way_of_communication = models.ForeignKey(WayOfCommunication)

    recipient = models.ForeignKey(Patient)
    
    def __unicode__(self):
        return "%s %s" % (unicode(self.recipient), self.way_of_communication.verbose_name)
    
    def get_data_for_sending(self):
        """
        Prepare OutputData for selected way_of_communication.
        Return an object of a subclass of OutputData.
        """
        
        call = "self.get_data_for_%s()" % self.way_of_communication.name      
        logger.info("sendable.get_data_for_sending() calling method: " + call)        
        return eval(call)
        
    def create_scheduled_event(self, send_time):
        """
        Create a scheduled event for a specific send_time
        @param send_time: Datetime object with the time of the reminder 
        """        
        scheduled_event = ScheduledEvent(sendable = self,
                                         send_time = send_time)
        scheduled_event.save()


class ScheduledEvent(models.Model):
    """
    Define a ScheduledEvent for sending at a specific date.
    """
    def __unicode__(self):
        return "Scheduled " + self.sendable.way_of_communication.verbose_name + ": " +  self.sendable.recipient.phone_number \
            + " (" + str(self.send_time) + ")"
 
    sendable_type = models.ForeignKey(ContentType)
    sendable_id = models.PositiveIntegerField()
    sendable = generic.GenericForeignKey('sendable_type', 'sendable_id')
    filename = models.CharField(max_length=255, blank=True, null=True)
    retry = models.PositiveIntegerField(default=0)

    send_time = models.DateTimeField()

    STATES = (
        ('new','new'),
        ('pending','pending'),
        ('queued', 'queued'),
        ('done', 'done'),
        ('failed','failed'),
    )

    state = models.CharField(max_length = 10,
                             choices = STATES,
                             default = 'new')                             


class AuthenticationCall(models.Model):
    """
    Queues all calls that were made to authenticate a user via his 
    mobile phone number. These calls get deleted once the user has
    been authenticated successfully.
    """
    
    number = models.CharField(max_length = 20)
    time = models.DateTimeField(auto_now_add = True)
