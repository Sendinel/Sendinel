from math import floor
from string import Template


def generate_sms(sms_parts):
    parts_length = get_parts_length
    if len(sms_parts) == 1:
    a_template = Template("$")
    elif len(specific_content) == 4:
    a_template = Template("Dear $name, please remember your appointment" + \
            " at the $hospital at %$date with doctor %doctor") 
        sms = generate_appointment_sms(specific_content, text)
    return sms
    
def get_parts_length(sms_parts):
    sum = 0
    for key,value in sms_parts:
        sum += len(value)
    return sum

def generate_message_sms(text):
    return text[0:160]
    
    
def generate_appointment_sms(specific_content,text):
    sms_static_text = text % (('',) * 4)
    chars_left = 160 - len(specific_content.get('date')) - len(text)
    
    max_length = int(floor(chars_left/3))

    sms =  text % (specific_content.get('name'), specific_content.get('hospital'), \
                    specific_content.get('date'),specific_content.get('doctor'))
  
    if len(sms) > 160:
        sms = text % (specific_content.get('name')[0:max_length],\
                        specific_content.get('hospital')[0:max_length], \
                        specific_content.get('date'),specific_content.get('doctor')[0:max_length])
                
    
    return sms

    
