from math import floor, ceil


def generate_text(contents, template, reduce = True):
    """
    creates an sms text from a given template that is not longer than 160 characters
    """
    contents = replace_dollar_signs(contents)
    sms = template.substitute(contents)
    if reduce:
        if len(sms) > 160:
            template_length = len(sms)-get_content_length(contents)
            new_contents = reduce_contents(contents, 160 - template_length)
            sms = template.substitute(new_contents)
    return sms
    
def get_content_length(contents):
    """ 
    returns the length of all dictionary values together 
    """
    length = 0
    for value in contents.itervalues():
        length += len(value)
    return length

def replace_dollar_signs(contents):
    """ 
    dollar signs are represented in a way, that they continue to be $, even after
    the substitution of the template
    """
    for value in contents.itervalues():
        value.replace("$","$$")
    return contents

def reduce_contents(contents, chars_left):
    """ 
    the inserted fields are shortened, 
    so that the sms will in total not ecceed 160 characters
    """
    #DATE FIELD IS HARD CODED NOW
    if 'date' in contents:
        chars_left -= len(contents ['date'])
        cut_length = int(floor(float(chars_left)/(len(contents) - 1)))
        # because date is not shortened, len(contents) must be one shorter
    else:
        cut_length = int(ceil(float(chars_left)/len(contents)))
    for key in contents.iterkeys():
        if key != 'date':
            contents[key] = contents[key][0:cut_length]
    return contents
