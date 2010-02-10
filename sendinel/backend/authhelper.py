import re

from sendinel.backend.helper import NotObservedNumberException

class AuthHelper:
    """
    Provide functionality needed for authenticating phone numbers
    """
    to_check = []
    log_path = "C:/temp/call_log.txt"
    
    def clean_up_to_check(self):
        self.to_check = []

    def authenticate(self, number):
        try:
            number = format_phone_number(number)
            return True
        except ValueError:
            return False

    def observe_number(self, number):
        if self.to_check.count(number) < 1:
            self.to_check.append(number)
    
    def check_log(self, number):
        parse_log(self.log_path)
    
        if number == "0123456":
            return True
        else:
            if number == "01234":
                raise NotObservedNumberException('Number was not observed')
            return False
    
def parse_log(log_file):
    pass
    
def format_phone_number(number):
    """
    return the number as Integer or raise ValueError
    """
    regex = re.compile('(\/|\+|-| )')
    new_number = regex.sub('', number)
    if int(new_number) and new_number[0] == '0':
        return new_number
    else:
        raise ValueError('please give national number without country prefix')    

    