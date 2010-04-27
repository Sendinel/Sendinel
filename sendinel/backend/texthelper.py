from sendinel.settings import SMS_SALUTATION

def date_to_text(weekday, day, month, hour, minutes):
    """
        Use:
        >>> date_to_text(3, 18, 3, 11, 40)
        {"date" : 'Wednesday, eighteenth of March', "time" : 'eleven forty'}
        
    """
    months = {1: "January",
             2: "February",
             3: "March",
             4: "April",
             5: "Mai",
             6: "June",
             7: "July",
             8: "August",
             9: "September",
             10:"October",
             11:"November",
             12:"December"}
             
    days =  {1: "Monday",
             2: "Tueday",
             3: "Wednesday",
             4: "Thursday",
             5: "Friday",
             6: "Saturday",
             7: "Sunday"}
             
    order = {1: "first",
             2: "second",
             3: "third",
             4: "fourth",
             5: "fifth",
             6: "sixth",
             7: "seventh",
             8: "eighth",
             9: "ninth",
             10:"tenth",
             11:"eleventh",
             12:"twelveth",
             13:"thirteenth",
             14:"fourteenth",
             15:"fifteenth",
             16:"sixteenth",
             17:"seventeenth",
             18:"eighteenth",
             19:"nineteenth",
             20:"twentieth",
             21:"twenty-first",
             22:"twenty-second",
             23:"twenty-third",
             24:"twenty-fourth",
             25:"twenty-fifth",
             26:"twenty-sixth",
             27:"twenty-seventh",
             28:"twenty-eighth",
             29:"twenty-ninth",
             30:"thirtieth",
             31:"thirty-first"}
    
    numbers = { 0:  "oh clock",
                1:  "one",
                2:  "two",
                3:  "three",
                4:  "four",
                5:  "five",
                6:  "six",
                7:  "seven",
                8:  "eigth",
                9:  "nine",
                10: "ten",
                11: "eleven",
                12: "twelve",
                13: "thirteen",
                14: "fourteen",
                15: "fifteen",
                16: "sixteen",
                17: "seventeen",
                18: "eighteen",
                19: "nineteen",
                20: "twenty",
                21: "twenty-one",
                22: "twenty-two",
                23: "twenty-three",
                24: "twenty-four",
                25: "twenty-five",
                26: "twenty-six",
                27: "twenty-seven",
                28: "twenty-eight",
                29: "twenty-nine",
                30: "thirty",
                31: "thirty-one",
                32: "thirty-two",
                33: "thirty-three",
                34: "thirty-four",
                35: "thirty-five",
                36: "thirty-six",
                37: "thirty-seven",
                38: "thirty-eigth",
                39: "thirty-nine",
                40: "forty",
                41: "forty-one",
                42: "forty-two",
                43: "forty-three",
                44: "forty-four",
                45: "forty-five",
                46: "forty-six",
                47: "forty-seven",
                48: "forty-eigth",
                49: "forty-nine",
                50: "fifty",
                51: "fifty-one",
                52: "fifty-two",
                53: "fifty-three",
                54: "fifty-four",
                55: "fifty-five",
                56: "fifty-six",
                57: "fifty-seven",
                58: "fifty-eigth",
                59: "fifty-nine"}
    
    text = {"date" : days[weekday] + ", " + order[day] + " of " + months[month],
            "time" : numbers[hour] + " " + numbers[minutes]}
    
    return  text 

def generate_text(contents, template, is_sms = True):
    """
    creates an sms text from a given template that is not longer than 160 characters
    """
    max_chars = 160 - len(SMS_SALUTATION)
    
    contents = replace_dollar_signs(contents)
    sms = template.substitute(contents)
    
    if is_sms:
        if len(sms) > max_chars:
            template_length = len(sms)-get_content_length(contents)
            new_contents = reduce_contents(contents, max_chars - template_length)       
            sms = SMS_SALUTATION + template.substitute(new_contents)
        else:
            sms = SMS_SALUTATION + sms
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
    important_content = ['date', 'time']
    
    important_content_counter = 0
    for field in important_content:
        if field in contents:
            chars_left -= len(contents[field])
            # because date is not shortened, len(contents) must be one shorter
            important_content_counter += 1    
    
    cut_length = int(chars_left/(len(contents)-important_content_counter))
    
    for key in contents.iterkeys():
        if not key in important_content:
            contents[key] = contents[key][0:cut_length]
            
    return contents
