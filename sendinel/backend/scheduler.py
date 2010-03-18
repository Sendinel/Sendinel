import time
import sys

from os.path import abspath, dirname
from datetime import datetime
from itertools import chain

from django.core.management import setup_environ

# fix paths for run from commandline
project_path = dirname(abspath(__file__)) + "/../../"
sys.path.insert(0, project_path)
from sendinel import settings
setup_environ(settings) # this must be run before any model etc imports

from sendinel.backend.models import ScheduledEvent, InfoMessage,\
                                    HospitalAppointment
from sendinel.logger import logger


def get_all_due_events():
    return ScheduledEvent.objects \
                    .filter(state__exact = 'new') \
                    .filter(send_time__lte=datetime.now())


def run(run_only_one_time = False):
    while True:        
                 
        dueEvents = get_all_due_events()
                         
        for event in dueEvents:
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
                if not run_only_one_time:
                    time.sleep(20)
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
