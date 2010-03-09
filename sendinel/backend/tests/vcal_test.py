from django.test import TestCase

from datetime import datetime, timedelta

from sendinel.backend.models import Hospital
from sendinel.backend.output import BluetoothOutputData
from sendinel.backend.vcal import *
class VcalTest(TestCase):
    """
    """
    
    def test_create_vcal_string(self):
        startDate = datetime(2010, 04, 04, 12, 00, 00)
        endDate = datetime(2010, 04, 04, 12, 30, 00)
        old_setting = settings.REMINDER_TIME_BEFORE_APPOINTMENT
        settings.REMINDER_TIME_BEFORE_APPOINTMENT = timedelta(minutes = 2000)
        location = Hospital(name = "aHospital")
        content = "aContent in some language"
        uid = 43
        vcalData = create_vcal_string(startDate, endDate, location, content, uid)
        self.assertEquals(vcalData,
"""BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
UID:43
SUMMARY:aContent in some language
DTSTART:20100404T120000Z
DTEND:20100404T123000Z
LOCATION:aHospital
BEGIN:VALARM
TRIGGER:-PT2000M
ACTION:DISPLAY
DESCRIPTION:aContent in some language
END:VALARM
END:VEVENT
END:VCALENDAR""")
        settings.REMINDER_TIME_BEFORE_APPOINTMENT = old_setting