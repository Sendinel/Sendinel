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
        self.assertContains(response, 'name="recipient"')
        self.assertNotContains(response, 'name="recipient_type"')
        self.assertNotContains(response, 'name="recipient_id"')

    def test_create_appointment_submit(self):
        number_of_appointments = HospitalAppointment.objects.count()
        response = self.client.post("/create_appointment/", 
                    {'date_0': '2012-08-12',
                    'date_1': '19:02:42',
                    'doctor': "1",
                    'hospital': '1',
                    'recipient': 'Shiko Taga'  })
        self.assertRedirects(response, reverse('index'))
        self.assertEquals(HospitalAppointment.objects.count(),
                            number_of_appointments + 1)
        appointment = HospitalAppointments.objects.reverse()[:1][0]
        self.assertEquals(appointment.hospital.id, 1)
        self.assertEquals(appointment.doctor.id, 1)
        self.assertEquals(appointment.recipient.name, 'Shiko Taga')
        self.assertEquals(appointment.date, datetime(2012,8,12,19,02,42))
        