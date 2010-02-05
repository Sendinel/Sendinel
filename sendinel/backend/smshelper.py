from math import floor

def generate_sms(specific_content, text):
    if len(specific_content) == 0:
        sms = generate_message_sms(text)
    elif len(specific_content) == 4:
        sms = generate_appointment_sms(specific_content, text)
    return sms

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

    
