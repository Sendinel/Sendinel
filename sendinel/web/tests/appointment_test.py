from datetime import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase

from sendinel.backend.models import *

class AppointmentViewTest(TestCase):
    fixtures = ['backend']
    urls = 'web.urls'
    
    def test_create_appointment(self):
        response = self.client.get("/create_appointment/")
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, 'name="date_0"')
        self.assertContains(response, 'name="date_1"')
        self.assertContains(response, 'name="doctor"')
        self.assertContains(response, 'name="hospital"')
        self.assertContains(response, 'name="recipient_name"')
        self.assertNotContains(response, 'name="recipient_type"')
        self.assertNotContains(response, 'name="recipient_id"')

    def test_create_appointment_submit(self):
        number_of_appointments = HospitalAppointment.objects.count()
        response = self.client.post("/create_appointment/", 
                    {'date_0': '2012-08-12',
                    'date_1': '19:02:42',
                    'doctor': "1",
                    'hospital': '1',
                    'recipient_name': 'Shiko Taga',
                    'way_of_communication': 'sms'  })
        self.assertRedirects(response, reverse('index'))
        self.assertEquals(HospitalAppointment.objects.count(),
                            number_of_appointments + 1)
        appointment = HospitalAppointment.objects \
            .order_by("id").reverse()[:1][0]
        self.assertEquals(appointment.hospital.id, 1)
        self.assertEquals(appointment.doctor.id, 1)
        self.assertEquals(appointment.recipient.name, 'Shiko Taga')
        self.assertEquals(appointment.date, datetime(2012,8,12,19,02,42))
        self.assertEquals(appointment.way_of_communication, "sms")
    
    def test_create_appointment_submit_validations(self):
        response = self.client.post("/create_appointment/", 
                    {'date_0': 'abc',
                    'date_1': 'def',
                    'doctor': '',
                    'hospital': '',
                    'recipient_name': '',
                    'way_of_communication': 'xyz'  })
        self.failUnlessEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'hospital',
                            'This field is required.')
        self.assertFormError(response, 'form', 'doctor',
                            'This field is required.')
        self.assertFormError(response, 'form', 'recipient_name',
                            'This field is required.')
        self.assertFormError(response, 'form', 'date',
                            'Enter a valid date/time.')
        self.assertFormError(response, 'form', 'way_of_communication',
                            'Select a valid choice. xyz' \
                            + ' is not one of the available choices.')
                            
    def test_create_appointment_scheduled_event_sms(self):
        number_of_events = ScheduledEvent.objects.count()
        response = self.client.post("/create_appointment/", 
                    {'date_0': '2012-08-12',
                    'date_1': '19:02:42',
                    'doctor': "1",
                    'hospital': '1',
                    'recipient_name': 'Shiko Taga',
                    'way_of_communication': 'sms'  })
        self.assertEquals(ScheduledEvent.objects.count(),
                            number_of_events + 1)
    
        
    def test_create_appointment_scheduled_event_bluetooth(self):
        number_of_events = ScheduledEvent.objects.count()
        response = self.client.post("/create_appointment/", 
                    {'date_0': '2012-08-12',
                    'date_1': '19:02:42',
                    'doctor': "1",
                    'hospital': '1',
                    'recipient_name': 'Shiko Taga',
                    'way_of_communication': 'bluetooth'  })
        self.assertEquals(ScheduledEvent.objects.count(),
                            number_of_events)