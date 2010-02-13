import re
from time import time

from sendinel.backend.helper import NotObservedNumberException

class AuthHelper:
    """
    Provide functionality needed for authenticating phone numbers
    """
    to_check = {}
    log_path = "C:/temp/call_log.txt"
    
    """
    delete all entries 
    """
    def clean_up_to_check(self):
        self.to_check = {}
        
    def delete_old_numbers(self):
        to_delete = []
        for key in self.to_check:
            if self.to_check[key]["time"]<(time()-180):
                to_delete.append(key)
        for entry in to_delete:
            del(self.to_check[entry])

    def authenticate(self, number):
        try:
            number = format_phone_number(number)
            return True
        except ValueError:
            return False

    def observe_number(self, number):
        if not self.to_check.has_key(number):
            self.to_check[number] = {"has_called" : False, "time" : time()}
    
    def check_log(self, number):
        self.delete_old_numbers
        self.parse_log(self.log_path)
    
        if self.to_check.has_key(number):
            return self.to_check[number]["has_called"]
        else:
            raise NotObservedNumberException('Number was not observed')
    
    def parse_log(self, log_file):
        log = open(log_file)
        for entry in log:
            (timestamp, datetime, phone, called_number) = entry.split("\t")
            if self.to_check.has_key(phone):
                self.to_check[phone]["has_called"] = True
        log.close()
        
        log = open(log_file, "w")
        log.write("")
        log.close()
        
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

    