from django.test import TestCase
from datetime import datetime

from sendinel.backend.models import ScheduledEvent
from sendinel.backend import scheduler
from sendinel.backend import output

class SchedulerTest(TestCase):
    
    counter = 0
    
    fixtures = ['backend']
    
    def test_scheduler(self):
        
        def scheduled_events_count(state = 'new'):
            return ScheduledEvent.objects \
                                 .filter(state__exact = state) \
                                 .filter(send_time__lte=datetime.now()) \
                                 .count()
        def send(data):
            SchedulerTest.counter += 1
        
        scheduled_events_counter = scheduled_events_count()
        SchedulerTest.counter = 0
        scheduler.send = send
        scheduler.run(run_only_one_time = True)
        
        # assert that all scheduled events have been processed by send()
        self.assertEquals(scheduled_events_counter, SchedulerTest.counter)
        # assert that no events with state new exist anymore
        self.assertEquals(scheduled_events_count(), 0)
        