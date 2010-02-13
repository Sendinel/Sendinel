import re
from time import time

from sendinel.backend.helper import NotObservedNumberException

class AuthHelper:
    """
    Provide functionality needed for authenticating phone numbers
    """
    to_check = {}
    log_path = "C:/temp/call_log.txt"
    
   
    def clean_up_to_check(self):
        """
        delete all entries from the observation list 
        """
        self.to_check = {}
        
    def delete_old_numbers(self):
        """
        Delete all entries from the observation list that are 
        older than three minutes
        """
        to_delete = []
        
        # you first have to collect all values that
        # have to be deleted because otherwise
        # the iteration would crash
        for key in self.to_check:
            if self.to_check[key]["time"] < (time()-180):
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
        """
        add the given number to the observation list
        if it is already in the list, update the timestamp
        
        @param  number: the phone number to be observed
        @type   number: string        
        """
        if not self.to_check.has_key(number):
            self.to_check[number] = {"has_called" : False, "time" : time()}
        else:
            self.to_check[number]["time"] = time() 
    
    def check_log(self, number):
        """
        answer whether the given number has already called
        
        @param  number:     telephone number to check
        @type   number:     string
        
        @raise NotObservedNumberException: if the given number is not observed
               (oberservation may have timed out)
        """
        self.delete_old_numbers()
        self.parse_log(self.log_path)
    
        if self.to_check.has_key(number):
            return self.to_check[number]["has_called"]
        else:
            raise NotObservedNumberException('Number was not observed')
    
    def parse_log(self, log_file):
        """
        Check the given asterisk log file for calls and
        for observed phone numbers update status.
        afterwards empty the log file
        
        @param  log_file:   file path to the asterisk call log file
        @type   log_file:   string
        """
        log = open(log_file)
        for entry in log:
            (timestamp, datetime, phone, called_number) = entry.split("\t")
            if self.to_check.has_key(phone):
                self.to_check[phone]["has_called"] = True
        log.close()
        
        # Empty the log file
        log = open(log_file, "w")
        log.write("")
        log.close()
    
def format_phone_number(number):
    """
    Replaces all number specific characters like
    "+", "-" and "/" and checks that there are no
    letters included.
    
    @param  number:     The phone number that will be checked
    @type   number:     string
    
    @raise  ValueError
    """
    regex = re.compile('(\/|\+|-| )')
    new_number = regex.sub('', number)
    
    # if the conversion to int does not fail
    # then there are only numbers included
    # in the string
    if int(new_number) and new_number[0] == '0':
        return new_number
    else:
        raise ValueError('please give national number without country prefix')    

    