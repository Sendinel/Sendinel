import time
import sys

from os.path import abspath, dirname
from datetime import datetime, timedelta

from django.core.management import setup_environ

# fix paths for run from commandline
PROJECT_PATH = dirname(abspath(__file__)) + "/../../"
sys.path.insert(0, PROJECT_PATH)
from sendinel import settings
setup_environ(settings) # this must be run before any model etc imports

from sendinel.backend.models import ScheduledEvent
from sendinel.logger import logger

def openFile(filename):
    """
        Open the specified file; wrapping needed so tests can run

        @param filename: Filename of the file to be opened
        @type  filename: String

        @return A file object
    """
    return open(filename)

def get_spoolfile_status(filename):
    """
        Get the status of a spooled Asterisk operation
        
        @param filename: Filename of the Spool file
        @type  filename: String
    """
    filename = settings.ASTERISK_DONE_SPOOL_DIR + filename
    spoolfile = openFile(filename)
    while True:
        line = spoolfile.readline()
        if not line:
            status = "Queued"
            break
        try:
            (key, value) = line.split(":", 1)
        except:
            (key, value) = (None, None)
        if key == "Status":
            status = value.strip()
            break
    return status

def get_all_due_events():
    """
        Get all scheduled events from the database that are due

        @return All due elements
    """
    return ScheduledEvent.objects \
                    .filter(state__exact = 'new') \
                    .filter(send_time__lte=datetime.now())

def get_all_queued_events():
    """
        Get all scheduled events from the database that are queued

        @return All queued elements
    """
    return ScheduledEvent.objects \
                    .filter(state__exact = 'queued')

def check_spool_files():
    """
        Check all queued spoolfiles if they have already been processed
        by the Asterisk telephony server;
        Set the corresponding status for the scheduled events
    """
    queued_events = get_all_queued_events()
    for event in queued_events:
        try:
            status = get_spoolfile_status(event.filename)
            if status == "Completed":
                logger.info("Completed sending %s" % unicode(event.sendable))
                event.state = "done"
            elif status == "Expired":
                # Handle what to do if asterisk gave up
                event.retry += 1
                if event.retry < settings.ASTERISK_RETRY:
                    logger.info("%s expired; rescheduling" % unicode(event.sendable))
                    event.send_time = datetime.now() + \
                        timedelta(minutes = settings.ASTERISK_RETRY_TIME)
                    event.state = "new"
                else:
                    event.state = "failed"
                    logger.error("Sending %s failed" % unicode(event.sendable))
            elif status == "Failed":
                # Something really, really went wrong
                event.state = "failed"
                logger.error("Sending %s failed" % unicode(event.sendable))
            event.save()
        except:
            # This means the file has not been found in the done folder
            # nothing has to be done here.
            pass

def run(run_only_one_time = False):
    """
        check every second, if an SMS or a Voicecall needs to be sent
        and send it if due
    """
    while True:
        check_spool_files()         
        due_events = get_all_due_events()
                         
        for event in due_events:
            event.state = 'pending'
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
            if len(get_all_queued_events()) > 0:
                break

            try:                
                logger.info("  sending: %s" % unicode(data))
                event.filename = data.send()
                #if not run_only_one_time:
                    #time.sleep(20)
            except Exception, e:
                logger.error("Failed to send: " + unicode(data) + \
                             " exception " + unicode(e))
                event.state = "failed"
                event.save()
                    
            event.state = 'queued'
            event.save()
            del data
        del due_events
            #TODO Exception Handling
        if run_only_one_time: 
             break
        time.sleep(1)


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

    
