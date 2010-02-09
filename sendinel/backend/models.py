from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
import smshelper
from output import *

class User(models.Model):
    """
    Define an interface for a user of the system.
    """
    class Meta:
        abstract = True
    name = models.CharField(max_length=255)
    
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
    pass



class Hospital(models.Model):
    """
    Represent a Hospital.
    """
    name = models.CharField(max_length=255)
    



class Sendable(models.Model):
    """
    Define an interface for a Sendable object.
    """
    WAYS_OF_COMMUNICATION = (
        ('sms','SMS'),
        ('bluetooth','Bluetooth'),
        ('voice','Voice Call'),
    )
    way_of_communication = models.CharField(max_length=9, choices=WAYS_OF_COMMUNICATION)
    
    def get_data_for_bluetooth():
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
    
    def get_data_for_voice():
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
    patient = models.ForeignKey(Patient)
    
    def get_data_for_bluaetooth():
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
        data.data = smshelper.generate_appointment_sms(str(self.date),
                                            self.doctor.name,
                                            self.hospital.name,
                                            self.patient.name)
        data.phone_number = self.patient.phone_number
        return data

    def get_data_for_voice():
        """
        Prepare OutputData for voice.
        Return VoiceOutputData for sending.
        TODO Not implemented yet.
        """
        pass
    
    
class ScheduledEvent(models.Model):
    """
    Define a ScheduledEvent for sending at a specific date.
    """    
    sendable_type = models.ForeignKey(ContentType)
    sendable_id = models.PositiveIntegerField()
    sendable = generic.GenericForeignKey('sendable_type', 'sendable_id')

    send_time = models.DateTimeField()

    STATES= (
        ('new','new'),
        ('sent','sent'),
        ('failed','failed'),
    )
    state = models.CharField(max_length = 1, choices = STATES, default = 'new')
    

