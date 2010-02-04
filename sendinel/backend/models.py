from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
import smshelper

class OutputData:
    data = None

class BluetoothOutputData(OutputData):
    url = None

class SMSOutputData(OutputData):
    phone_number = None

class VoiceOutputData(OutputData):
    phone_number = None


class User(models.Model):
    class Meta:
        abstract = True
    name = models.CharField(max_length=255)
    
class Doctor(User):
    pass

class Patient(User):
    phone_number = models.CharField(max_length=20)
    pass

class Hospital(models.Model):
    name = models.CharField(max_length=255)
    

class Sendable(models.Model):
    WAYS_OF_COMMUNICATION = (
        ('sms','SMS'),
        ('bluetooth','Bluetooth'),
        ('voice','Voice Call'),
    )
    way_of_communication = models.CharField(max_length=9, choices=WAYS_OF_COMMUNICATION)
    
    def get_data_for_bluetooth():
        pass
    
    def get_data_for_sms(self):
        pass
    
    def get_data_for_voice():
        pass
    
    def get_data_for_sending(self):
        return eval("self.get_data_for_%s()" % self.way_of_communication)

class ScheduledEvent(models.Model):
    
    sendable_type = models.ForeignKey(ContentType)
    sendable_id = models.PositiveIntegerField()
    sendable = generic.GenericForeignKey('sendable_type', 'sendable_id')

    send_time = models.DateTimeField()

    STATES= (
        ('N','New'),
        ('S','Sent'),
    )
    state = models.CharField(max_length=1, choices=STATES)
   
class HospitalAppointment(Sendable):
    date = models.DateTimeField()
    doctor = models.ForeignKey(Doctor)
    hospital = models.ForeignKey(Hospital)
    patient = models.ForeignKey(Patient)
    
    def get_data_for_bluaetooth():
        pass
    
    def get_data_for_sms(self):
        data = SMSOutputData()
        data.data = smshelper.generate_appointment_sms(str(self.date),
                                            self.doctor.name,
                                            self.hospital.name,
                                            self.patient.name)
        data.phone_number = self.patient.phone_number
        return data

    def get_data_for_voice():
        pass
    

    

