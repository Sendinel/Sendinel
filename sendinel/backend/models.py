from string import Template

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from sendinel.settings import DEFAULT_HOSPITAL_NAME, \
                              REMINDER_TIME_BEFORE_APPOINTMENT, \
                              BLUETOOTH_SERVER_ADDRESS  
from sendinel.backend import texthelper, vcal
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
    
class Doctor(User):
    """
    Represent a doctor.
    """
    pass

class Patient(User):
    """
    Represent a patient.
    """
    phone_number = models.CharField(max_length = 20)
    
    def __unicode__(self):
        return self.name or "unnamed patient"

    def infoservices(self):
        return InfoService.objects.filter(members__id = self.id)

class Hospital(models.Model):
    """
    Represent a Hospital.
    """
    name = models.CharField(max_length=255)
    current_hospital = models.BooleanField()
    
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
        
class InfoService(models.Model):
    """
    Represent a user group.
    Raises integrity error
    """
    members = models.ManyToManyField(Patient, through="Subscription")
    name = models.CharField(max_length=255, unique=True, blank=False, \
                            null=False)


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

    recipient = models.ForeignKey(Patient)
    
    def __unicode__(self):
        return "%s %s" % (unicode(self.recipient), self.way_of_communication)
    
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
        call = "self.get_data_for_%s()" % self.way_of_communication      
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

class HospitalAppointment(Sendable):
    """
    Define a HospitalAppointment.
    """
    
    date = models.DateTimeField()
    doctor = models.ForeignKey(Doctor)
    hospital = models.ForeignKey(Hospital)
    template = Template("Dear $name, please remember your appointment" + \
                         " at the $hospital at $date with doctor $doctor")
    def __unicode__(self):
        return "%s Doctor %s" % ((str(self.date) or ""), (str(self.doctor) or ""))
                         
    def get_data_for_bluetooth(self):
        """
        Prepare OutputData for voice.
        Generate the message for an HospitalAppointment.
        Return BluetoothOutputData for sending.

        """
        logger.info("starting get_data_for_bluetooth() in HospitalAppointment")
        
        data = BluetoothOutputData()
        data.bluetooth_mac_address = self.bluetooth_mac_address
        data.server_address = BLUETOOTH_SERVER_ADDRESS
        
        logger.info("Sending to Bluetooth Mac Address " + data.bluetooth_mac_address +
                    " and Bluetooth Server " + data.server_address)
        
        try:
            self.hospital
        except Hospital.DoesNotExist:
            self.hospital = Hospital.get_current_hospital()
        
        content = "Please remember your Appointment tomorrow at "\
                    + self.hospital.name\
                    + " by doctor "\
                    + self.doctor.name
        uid = vcal.get_uid()
        data.data = vcal.create_vcal_string(self.date, 
                                            self.hospital, 
                                            content,
                                            uid)
                                            
        logger.info("Created vCal with uid %s" % str(uid))
        logger.debug("Created vCal: " + data.data)
        
        return data

 
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

    def create_scheduled_event(self, send_time=None):
        """
        Create a scheduled event for sending a reminder for an appointment. 
        @param send_time: Datetime object with the time of the reminder
        If send_time is not give, REMINDER_TIME_BEFORE_APPOINTMENT is used.
        Calls Sendable.create_scheduled_event() to create the ScheduledEvent
        """
        if not send_time:      
            send_time = self.date - REMINDER_TIME_BEFORE_APPOINTMENT
        super(HospitalAppointment, self).create_scheduled_event(send_time)
       
    def save_with_patient(self, patient):
        """
        Save appointment with patient & hospital and create a scheduled event
        """
        patient.save()
        self.hospital = Hospital.get_current_hospital()
        self.recipient = patient
                
        self.save()
        self.create_scheduled_event()    
        return self
        
class InfoMessage(Sendable):
    """
    Define a InfoMessage.
    """
    #TODO extract to superclass?
    template = Template("$text")
    # TODO restrict text to 160? but not good for voice calls
    text = models.TextField()
    
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
    
class Subscription(models.Model):
    
    patient = models.ForeignKey(Patient)
    infoservice = models.ForeignKey(InfoService)
    
    way_of_communication = models.CharField(max_length=9,
                                choices=Sendable.WAYS_OF_COMMUNICATION)