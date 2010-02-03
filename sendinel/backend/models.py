from django.db import models
import smshelper

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
    
    def get_data_for_bluetooth():
        pass
    
    def get_data_for_sms():
        pass
    
    def get_data_for_voice():
        pass
        

class ScheduledEvent(models.Model):
    schedulable = models.ForeignKey(Sendable, primary_key=True)
    send_time = models.DateTimeField()
    WAYS_OF_COMMUNICATION = (
        ('sms','SMS'),
        ('bluetooth','Bluetooth'),
        ('voice','Voice Call'),
    )
    way_of_communication = models.CharField(max_length=9, choices=WAYS_OF_COMMUNICATION)
    STATES= (
        ('N','New'),
        ('S','Sent'),
    )
    state = models.CharField(max_length=1, choices=STATES)
    def send():
        pass
    
class HospitalAppointment(Sendable):
    date = models.DateTimeField()
    doctor = models.ForeignKey(Doctor)
    hospital = models.ForeignKey(Hospital)
    patient = models.ForeignKey(Patient)
    
    def get_data_for_bluetooth():
        pass
    
    def get_data_for_sms():
        #smshelper.generate_appointment_sms(str(date), doctor.name,
        #                                    hospital.name, patient.name)
        pass
        #return 
    
    def get_data_for_voice():
        pass
    

    

