from math import floor, ceil
from string import Template
import pdb


    
def generate_sms(contents, template):
    #template aus self wenn in klasse
    contents = replace_dollar_signs(contents)
    sms = template.substitute(contents)
    if len(sms) > 160:
        template_length = len(sms)-get_content_length(content)
        new_contents = reduce_contents(contents, 160 - template_length)
        sms = template.substitute(new_contents)
    return sms
    
def get_content_length(contents):
    length = 0
    for value in contents.itervalue():
        length += len(value)
    return length

def replace_dollar_signs(contents):
    for value in contents.itervalues():
		value.replace("$","$$")
    return contents

def reduce_contents(contents, signs_left):
    #DO NOT SHORTEN DATA FIELD
	cut_length =int(ceil(float(signs_left)/len(contents)))
	for value in contents.itervalue():
		value = value[0:cut_length]
	return contents



    
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

    
