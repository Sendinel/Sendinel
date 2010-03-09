import time

from datetime import datetime
from itertools import chain

from django.core.management import setup_environ

from sendinel import settings
from sendinel.backend.models import ScheduledEvent, InfoMessage,\
                                    HospitalAppointment
from sendinel.logger import logger

setup_environ(settings)

def get_all_due_events():
    due_events_1 = InfoMessage.objects \
                    .filter(state__exact = 'new') \
                    .filter(send_time__lte=datetime.now())
                    
    due_events_2 = HospitalAppointment.objects \
                     .filter(state__exact = 'new') \
                     .filter(send_time__lte=datetime.now())
                     
    #import pdb; pdb.set_trace()                 
    
    return due_events_1 | due_events_2

def run(run_only_one_time = False):
    while True:        
                         
        for event in get_all_due_events():
            try:
                data = event.sendable.get_data_for_sending()
                logger.info("Trying to send: %s" % str(event.sendable))
            except Exception as e:
                logger.error("Failed to get data for " + str(event) + \
                             " exception " + str(e))
                
                event.state = "failed"
                event.save()
                continue
            
            # TODO error handling
            try:
                logger.info("  sending: %s" % str(data))
                data.send()
            except Exception as e:
                logger.error("Failed to send: " + str(data) + \
                             " exception " + str(e))
                event.state = "failed"
                event.save()
                    
            
            event.state = 'sent'
            event.save()
            del data
        del dueEvents
            #TODO Exception Handling
        if run_only_one_time: break
        time.sleep(5)


if __name__ == "__main__":
    run()