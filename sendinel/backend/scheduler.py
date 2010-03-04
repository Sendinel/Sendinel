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
            data = event.sendable.get_data_for_sending()
            # TODO error handling
            try:
                for entry in data:
                    entry.send()
            except:
                print "Failed to send: " + str(entry)
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