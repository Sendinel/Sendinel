from math import floor
from string import Template


    
def generate_sms(contents, template):
    """
        Return an sms text as string from a given template that is not 
        longer than 160 characters. Substitute all placeholders in template
        with their corresponding entry in contents.

        @param contents: Dictionary with specific information
        @param template: Template for the SMS with placeholders

        >>> generate_sms({'date': "10.2.09",
                      'hospital': "Your Hospital"},
                     Template("go $date to $hospital"))
        ("go 10.2.09 to Your Hospital")
    """

    contents = replace_dollar_signs(contents)
    sms = template.substitute(contents)
    if len(sms) > 160:
        template_length = len(sms)-get_content_length(contents)
        new_contents = reduce_contents(contents, 160 - template_length)
        sms = template.substitute(new_contents)
    return sms
    
def get_content_length(contents):
    """ returns the length of all dictionary values together """
    length = 0
    for value in contents.itervalues():
        length += len(value)
    return length

def replace_dollar_signs(contents):
    """ dollar signs are represented in a way, that they continue to be $, even after
        the substitution of the template
    """
    for value in contents.itervalues():
		value.replace("$","$$")
    return contents

def reduce_contents(contents, chars_left):
    """ the inserted fields are shortened, 
        so that the sms will in total not ecceed 160 characters
    """
    #DATE FIELD IS HARD CODED NOW
    if 'date' in contents:
        cut_length =int(floor(float(chars_left - len(contents ['date']))/(len(contents) - 1)))
    else:
        cut_length =int(ceil(float(chars_left)/len(contents)))
    for key in contents.iterkeys():
        if key != 'date':
            contents[key] = contents[key][0:cut_length]
    return contents



    
def generate_appointment_sms(specific_content,text):
    """ generates an appointment sms from a given string text. 
    not currently used
    """
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

    
