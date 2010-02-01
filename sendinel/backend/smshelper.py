from math import floor

def generate_appointment_sms(date, doctor, hospital, name):
    sms_format = "Dear %s, please remember your appointment" + \
                " at the %s at %s with doctor %s"
    
    sms_static_text = sms_format % (('',) * 4)
    chars_left = 160 - len(date) - len(sms_static_text)
    
    max_length = int(floor(chars_left/3))

    sms =  sms_format % (name, hospital, date, doctor)
  
    if len(sms) > 160:
        sms = sms_format % (name[0:max_length], hospital[0:max_length], date, doctor[0:max_length])
    
    return sms

    
