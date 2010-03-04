from datetime import datetime
from string import Template

from django.db import models, IntegrityError
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from sendinel import settings
from sendinel.backend import texthelper
from sendinel.backend.output import *


class User(models.Model):
    """
    Define an interface for a user of the system.
    """
    class Meta:
        abstract = True
    name = models.CharField(max_length=255)
   
    
    def __unicode__(self):
        return self.name
    
class Doctor(User):
    """
    Represent a doctor.
    """
    pass

class Patient(User):
    """
    Represent a patient.
    """
    phone_number = models.CharField(max_length=20)
    
    def groups(self):
        return Usergroup.objects.filter(members__id = self.id)


class Hospital(models.Model):
    """
    Represent a Hospital.
    """
    name = models.CharField(max_length=255)
    current_hospital = models.BooleanField()
    
    def __unicode__(self):
        return self.name
        
        
class Usergroup(models.Model):
    """
    Represent a user group.
    Raises integrity error
    """
    members = models.ManyToManyField(Patient)
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)

    def __unicode__(self):
        return self.name
    

class Sendable(models.Model):
    """
    Define an interface for a Sendable object.
    """
    class Meta:
        abstract = True

    WAYS_OF_COMMUNICATION = (
        ('sms','SMS'),
        ('bluetooth','Bluetooth'),
        ('voice','Voice Call'),
    )
    way_of_communication = models.CharField(max_length=9,
                                choices=WAYS_OF_COMMUNICATION)

    recipient_type = models.ForeignKey(ContentType)
    recipient_id = models.PositiveIntegerField()
    recipient = generic.GenericForeignKey('recipient_type', 'recipient_id')
    
    def get_data_for_bluetooth(self):
        """
        Prepare OutputData for bluetooth.
        Return BluetoothOutputData for sending.
        """
        pass
    
    def get_data_for_sms(self):
        """
        Prepare OutputData for sms.
        Return SMSOutputData for sending.
        """
        pass
    
    def get_data_for_voice(self):
        """
        Prepare OutputData for voice.
        Return VoiceOutputData for sending.
        """
        pass
    
    def get_data_for_sending(self):
        """
        Prepare OutputData for selected way_of_communication.
        Return an object of a subclass of OutputData.
        """
        return eval("self.get_data_for_%s()" % self.way_of_communication)
        
    def create_scheduled_event(self, send_time):
        """
            Creates a ScheduledEvent for the Sendable at the given send_time.
        """
        scheduled_event = ScheduledEvent(sendable = self,
                                         send_time = send_time)
        scheduled_event.save()

class HospitalAppointment(Sendable):
    """
    Define a HospitalAppointment.
    """
    date = models.DateTimeField()
    doctor = models.ForeignKey(Doctor)
    hospital = models.ForeignKey(Hospital)
    template = Template("Dear $name, please remember your appointment" + \
                         " at the $hospital at $date with doctor $doctor")
    
    def get_data_for_bluetooth(self):
        """
            Prepare OutputData for voice.
            Generate the message for an HospitalAppointment.
            Return BluetoothOutputData for sending.

            TODO: Implement it...
   	"""
	pass
 
    def get_data_for_sms(self):
        """
        Prepare OutputData for sms.
        Generate the message for an HospitalAppointment.
        Return SMSOutputData for sending.
        """
        data = SMSOutputData()
        contents = {'date':str(self.date),
                    'name': self.recipient.name,
                    'doctor': self.doctor.name,
                    'hospital': self.hospital.name}
                    
        data.data = texthelper.generate_text(contents,
                        HospitalAppointment.template)
        data.phone_number = self.recipient.phone_number
        
        return data

    def get_data_for_voice(self):
        """
        Prepare OutputData for voice.
        Generate the message for an HospitalAppointment.
        Return VoiceOutputData for sending.
        """
        data = VoiceOutputData()
        contents = {'date':str(self.date),
                    'name': self.recipient.name,
                    'doctor': self.doctor.name,
                    'hospital': self.hospital.name}

        data.data = texthelper.generate_text(contents,
                        HospitalAppointment.template, False)
        data.phone_number = self.recipient.phone_number

        return data

    def create_scheduled_event(self):
        """
            Create a scheduled event for sending a reminder before an
            appointment. The time before the appointment is used as specified
            in the settings:
            REMINDER_TIME_BEFORE_APPOINTMENT specified as timedelta object.
        """
        send_time = self.date - settings.REMINDER_TIME_BEFORE_APPOINTMENT
        Sendable.create_scheduled_event(self, send_time)

class TextMessage(Sendable):
    """
    Define a TextMessage.
    """
    template = Template("$text")
    # TODO restrict text to 160? but not good for voice calls
    text = models.TextField()
    
    
    def get_data_for_sms(self):
        """
        Prepare OutputData for sms.
        Generate the message for an HospitalAppointment.
        Return SMSOutputData for sending.
        """
        
        data = SMSOutputData()            
        data.data = texthelper.generate_text({'text': self.text},
                                            TextMessage.template)
        data.phone_number = self.recipient.phone_number
        
        return data
    
    
class ScheduledEvent(models.Model):
    """
    Define a ScheduledEvent for sending at a specific date.
    """    
    sendable_type = models.ForeignKey(ContentType)
    sendable_id = models.PositiveIntegerField()
    sendable = generic.GenericForeignKey('sendable_type', 'sendable_id')

    send_time = models.DateTimeField()

    STATES = (
        ('new','new'),
        ('sent','sent'),
        ('failed','failed'),
    )
    state = models.CharField(max_length = 3,
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
    

    
               


