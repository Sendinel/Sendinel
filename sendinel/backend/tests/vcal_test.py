from django.test import TestCase

from datetime import datetime, timedelta

from sendinel.backend.models import Hospital, HospitalAppointment
from sendinel.backend.output import BluetoothOutputData
from sendinel.backend import vcal
from sendinel import settings

class VcalTest(TestCase):
    """
    """
    
    fixtures = ['backend']

    class FakeDatetime:
        def now(self):
            return datetime(2010, 4, 4)
        
    
    def test_create_vcal_string(self):
        startDate = datetime(2010, 04, 04, 12, 00, 00)
        location = Hospital(name = "aHospital")
        content = "aContent in some language"
        uid = "43"        
        
        vcal.settings.REMINDER_TIME_BEFORE_APPOINTMENT \
                = timedelta(days = 1)
                
        vcal.datetime = self.FakeDatetime()
            
        vcalData = vcal.create_vcal_string(startDate, location, content, uid)
        self.assertEquals(vcalData,
"""BEGIN:VCALENDAR
VERSION:1.0
BEGIN:VEVENT
UID:43
DTSTART:20100404T120000Z
DTEND:20100404T130000Z
DESCRIPTION:aContent in some language
SUMMARY:aContent in some language
DTSTAMP:20100404T000000Z
LOCATION:aHospital
DALARM:20100403T120000Z
AALARM:20100403T120000Z
END:VEVENT
END:VCALENDAR""")
        vcal.settings = settings
        vcal.datetime = datetime
        
    def test_get_uid(self):    
        vcal.datetime = self.FakeDatetime()
        
        result = vcal.get_uid()
        string = self.FakeDatetime().now().strftime("%Y%m%dT%H%M%S")
        string += "@" + settings.VCAL_UID_SLUG
        
        self.assertEquals(result, string)
        
        vcal.datetime = datetime