import re
from time import time

from sendinel.backend.models import *
from sendinel.backend.helper import NotObservedNumberException

class AuthHelper:
    """
    Provide functionality needed for authenticating phone numbers
    """
    to_check = {}
    log_path = "/tmp/call_log.txt"
    
   
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

    def authenticate(self, number, name):
        """
        Write the number to the observation list and return
        the number as it will be observed
        
        @param  number:     Phone number (may contain special chars)
        @type   number:     String
        
        @return Phone number without special chars on success
        """
        try:
            number = format_phone_number(number)
            self.observe_number(number, name)
            
            return number
        except ValueError:
            return False

    def observe_number(self, number, name):
        """
        add the given number to the observation list
        if it is already in the list, update the timestamp
        
        @param  number: the phone number to be observed
        @type   number: string        
        """
        
        # only use the last 7 digits of the number for the key
        
        if not self.to_check.has_key(number[-7:]):
            self.to_check[number[-7:]] = {"number" : number, "has_called" : False, "time" : time(), "name" : name}
        else:
            self.to_check[number[-7:]]["time"] = time() 
    
    def check_log(self, number):
        """
        answer whether the given number has already called
        if a number is successfully authenticated, add the person to the database
        
        @param  number:     telephone number to check
        @type   number:     string
        
        @raise NotObservedNumberException: if the given number is not observed
               (oberservation may have timed out)
        """
        self.delete_old_numbers()
        try:
            self.parse_log(self.log_path)
        except:
            open(self.log_path, 'w').close()
            self.parse_log(self.log_path)
    
        if self.to_check.has_key(number[-7:]):
            if self.to_check[number[-7:]]["has_called"]:
                person = Patient()
                person.phone_number = self.to_check[number[-7:]]["number"]
                person.name = self.to_check[number[-7:]]["name"]
                person.save()
                return True
            else:
                return False
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
            if self.to_check.has_key(phone[-7:]):
                self.to_check[phone[-7:]]["has_called"] = True
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

    