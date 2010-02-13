import time
from datetime import datetime
from django.core.management import setup_environ
from sendinel import settings
setup_environ(settings)

from sendinel.backend.models import ScheduledEvent
from sendinel.backend.output import send

def run(run_only_one_time = False):
    while True:
        dueEvents = ScheduledEvent.objects \
                        .filter(state__exact = 'new') \
                        .filter(send_time__lte=datetime.now())
        for event in dueEvents:
            data = event.sendable.get_data_for_sending()
            send(data)
            event.state = 'sent'
            event.save()
            del data
        del dueEvents
            #TODO Exception Handling
        if run_only_one_time: break
        time.sleep(5)


if __name__ == "__main__":
    run()