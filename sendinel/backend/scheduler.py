import time
from datetime import datetime
from django.core.management import setup_environ
from sendinel import settings
setup_environ(settings)

from sendinel.backend.models import ScheduledEvent

def run(run_only_one_time = False):
    while True:
        dueEvents = ScheduledEvent.objects \
                        .filter(state__exact = 'new') \
                        .filter(send_time__lte=datetime.now())
        for event in dueEvents:
            try:
                data = event.sendable.get_data_for_sending()
                print "Trying to send: %s" % str(event.sendable)
            except Exception as e:
                print "Failed to get data for " + event + " exception " + str(e)
                
                event.state = "failed"
                event.save()
                continue
            
            # TODO error handling
            try:
                for entry in data:
                    print "  sending: %s" % str(entry)
                    entry.send()
            except Exception as e:
                print "Failed to send: " + str(entry) + " exception " + str(e)
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