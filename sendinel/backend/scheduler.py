import time
import sys

from os.path import abspath, dirname
from datetime import datetime

from django.core.management import setup_environ

# fix paths for run from commandline
PROJECT_PATH = dirname(abspath(__file__)) + "/../../"
sys.path.insert(0, PROJECT_PATH)
from sendinel import settings
setup_environ(settings) # this must be run before any model etc imports

from sendinel.backend.models import ScheduledEvent
from sendinel.logger import logger


def get_all_due_events():
    """
        Get all scheduled events from the database that are due

        @return All due elements
    """
    return ScheduledEvent.objects \
                    .filter(state__exact = 'new') \
                    .filter(send_time__lte=datetime.now())


def run(run_only_one_time = False):
    while True:        
                 
        due_events = get_all_due_events()
                         
        for event in due_events:
            try:
                data = event.sendable.get_data_for_sending()
                logger.info("Trying to send: %s" % unicode(event.sendable))
            except Exception, e:
                logger.error("Failed to get data for " + unicode(event) + \
                             " exception " + unicode(e))
                
                event.state = "failed"
                event.save()
                continue
            
            # TODO error handling
            try:
                logger.info("  sending: %s" % unicode(data))
                data.send()
                #if not run_only_one_time:
                    #time.sleep(20)
            except Exception, e:
                logger.error("Failed to send: " + unicode(data) + \
                             " exception " + unicode(e))
                event.state = "failed"
                event.save()
                    
            
            event.state = 'sent'
            event.save()
            del data
        del due_events
            #TODO Exception Handling
        if run_only_one_time: 
             break
        time.sleep(5)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "Warning: Sendinel scheduler not running in daemon mode. " + \
                "Usage for daemon mode: %s <pid file>" % sys.argv[0]
        run()
    
    elif len(sys.argv) == 2:
        try:
            import daemon
            from daemon import pidlockfile
        except ImportError:
            print "Error: daemon and lockfile libraries are needed for" + \
                    " running the scheduler. " + \
                    " Install with: easy_install daemon; easy_install lockfile"
            exit(1)
    
        PID_FILE = sys.argv[1]
        WORKING_DIRECTORY = settings.PROJECT_PATH
    
        context = daemon.DaemonContext(
                    working_directory = WORKING_DIRECTORY,
                    pidfile = pidlockfile.PIDLockFile(PID_FILE),
                    detach_process = True)
    
        context.__enter__()
        try:
            run()
        finally:
            context.__exit()
    
    else:
        print "Usage: %s [pid file]\n  without pid file the scheduler " + \
                "won't run as daemon"

    
