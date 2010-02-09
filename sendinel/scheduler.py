import time
from datetime import datetime
from django.core.management import setup_environ
import settings
setup_environ(settings)

from backend.models import *
from backend.output import *


def run():
    while True:
        dueEvents = ScheduledEvent.objects \
                        .filter(state__exact = 'new') \
                        .filter(send_time__lte=datetime.now())
        for event in dueEvents:
            data =event.sendable.get_data_for_sending()
            print 'sending data: %s' % data
            send(data)
            event.state = 'sent'
            event.save()
            del data
        del dueEvents
            #TODO Exception Handling
        time.sleep(5)

if __name__ == "__main__":
    run()