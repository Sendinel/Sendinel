from datetime import datetime

from sendinel import settings

def create_vcal_string(start_date, location, content, uid):
    """
        Create valid content of an vcal file.
    
        @param  start_date:  Start Date of the appointment
        @type   start_date:  Datetime
        
        @param  location:   Location for the appointment
        @type   location:   String
        
        @param  content:    Subject of the appointment
        @type   content:    String
        
        @param  uid:        UID for the vcal entry
        @type   uid:        String
        
        @return:    Plain text version of the vcal entry
    """
    time_delta = settings.REMINDER_TIME_BEFORE_APPOINTMENT
    #need time difference in minutes for alarm
    alarm_time = start_date - time_delta
    end_date = start_date + settings.DEFAULT_APPOINTMENT_DURATION
    
    vcal_data = \
"""BEGIN:VCALENDAR
VERSION:1.0
BEGIN:VEVENT
UID:%(uid)s
DTSTART:%(start)s
DTEND:%(end)s
DESCRIPTION:%(content)s
SUMMARY:%(content)s
DTSTAMP:%(stamp)s
LOCATION:%(location)s
DALARM:%(alarm)s
AALARM:%(alarm)s
END:VEVENT
END:VCALENDAR""" % {\
    'uid': uid,
    'content': content,
    'location': location,
    'start': start_date.strftime("%Y%m%dT%H%M%S"),
    'end': end_date.strftime("%Y%m%dT%H%M%S"),
    'stamp': datetime.now().strftime("%Y%m%dT%H%M%S"),    
    'alarm': alarm_time.strftime("%Y%m%dT%H%M%S")}
    
    return vcal_data
    
def get_uid():
    """
        Calculate a unique UID for a vcal by using appointment id and a time.
    """
    date_time = datetime.now().strftime("%Y%m%dT%H%M%S")
    return "%s@%s" % (date_time, settings.VCAL_UID_SLUG)
    