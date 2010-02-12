from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
import smshelper
from string import Template
from sendinel.backend.output import *


class User(models.Model):
    """
    Define an interface for a user of the system.
    """
    class Meta:
        abstract = True
    name = models.CharField(max_length=255)
    
    def __str__(self):
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


class Hospital(models.Model):
    """
    Represent a Hospital.
    """
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name



class Sendable(models.Model):
    """
    Define an interface for a Sendable object.
    """
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
        Prepare OutputData for bluetooth.
        Return BluetoothOutputData for sending.
        TODO Not implemented yet.
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
                    
        data.data = smshelper.generate_sms(contents,
                        HospitalAppointment.template)
        data.phone_number = self.recipient.phone_number
        
        return data

    def get_data_for_voice(self):
        """
        Prepare OutputData for voice.
        Return VoiceOutputData for sending.
        TODO Not implemented yet.
        """
        pass
        
        
class TextMessage(Sendable):
    """
    Define a TextMessage.
    """
    template = Template("$text")
    # restrict text to 160? but not good for voice calls
    text = models.TextField()
    
    
    def get_data_for_sms(self):
        """
        Prepare OutputData for sms.
        Generate the message for an HospitalAppointment.
        Return SMSOutputData for sending.
        """
        
        data = SMSOutputData()            
        data.data = smshelper.generate_sms({'text': self.text},
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
    state = models.CharField(max_length = 1,
                             choices = STATES,
                             default = 'new')
    
    # def __init__(self, sendable, send_time):
        # self.sendable= sendable.id
        # self.send_time = send_time

