from string import Template

from django.db import models

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy

from sendinel.settings import REMINDER_TIME_BEFORE_APPOINTMENT
from sendinel.backend import texthelper, vcal
from sendinel.backend.models import Hospital, Sendable
from sendinel.backend.output import SMSOutputData, \
                                    VoiceOutputData, \
                                    BluetoothOutputData
from sendinel.logger import logger     

class NotificationType(models.Model):
    """
    Represent an appointment type like follow-up consultation.
    """
    
    name = models.CharField(max_length = 255)
    verbose_name = models.CharField(max_length = 255)
    template = models.CharField(max_length = 255)
    notify_immediately = models.BooleanField()

    def __unicode__(self):
        return self.verbose_name
    
    @classmethod
    def get_notification_type(cls, type_name):
        """
        Return the given NotificationType
        """
        
        notification_type = NotificationType.objects.get(name = type_name)
        
        return notification_type



class Notification(Sendable):
    """
    Define a Notification.
    """
    
    date = models.DateTimeField()
    notification_type = models.ForeignKey(NotificationType)
    hospital = models.ForeignKey(Hospital)
                         
    def __unicode__(self):
        return "Notification<%s>" \
                    % ((str(self.date) or ""))

    @property
    def template(self):
        return Template(self.notification_type.template)
        
    def reminder_text(self, contents = False, is_sms = True):
        """
        Return the generated reminder text
        """
        if not contents:
            contents = {'date': unicode(self.date.date()),
                        'time': unicode(self.date.time()),
                        'hospital': self.hospital.name}

        return texthelper.generate_text(contents,
                                        self.template, is_sms)

    def get_data_for_bluetooth(self):
        """
        Prepare OutputData for voice.
        Generate the message for an Notification.
        Return BluetoothOutputData for sending.

        """
        logger.info("starting get_data_for_bluetooth() in Notification")
        
        data = BluetoothOutputData()
        data.bluetooth_mac_address = self.bluetooth_mac_address
        data.server_address = self.bluetooth_server_address
        
        logger.info("Sending to Bluetooth Mac Address " + data.bluetooth_mac_address +
                    " and Bluetooth Server " + data.server_address)
        
        try:
            self.hospital
        except Hospital.DoesNotExist:
            self.hospital = Hospital.get_current_hospital()
        
        content = self.reminder_text()

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
        Generate the message for an Notification.
        Return SMSOutputData for sending.
        """

        data = SMSOutputData()
        data.data = self.reminder_text()
        data.phone_number = self.recipient.phone_number
        
        return data

    def get_data_for_voice(self):
        """
        Prepare OutputData for voice.
        Generate the message for an Notification.
        Return VoiceOutputData for sending.
        """
    
        spoken_date = texthelper.date_to_text(self.date.weekday() + 1, \
            self.date.day, self.date.month, self.date.hour, self.date.minute)

        data = VoiceOutputData()
        
        contents = {'date': unicode(spoken_date["date"]),
                    'time' : unicode(spoken_date["time"]),
                    'hospital': self.hospital.name}
                    
        data.data = self.reminder_text(contents, False)
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
        super(Notification, self).create_scheduled_event(send_time)
       
    def save_with_patient(self, patient):
        """
        Save appointment with patient & hospital and create a scheduled event
        """
        patient.save()

        self.recipient = patient
        self.save()
        self.create_scheduled_event()    
        return self