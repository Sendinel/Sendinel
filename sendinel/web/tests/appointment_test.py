from datetime import datetime
from sendinel.web.views import is_valid_appointment
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from sendinel.backend.models import ScheduledEvent, HospitalAppointment
from sendinel.backend.models import Hospital, Patient, AppointmentType
from sendinel import settings

class AppointmentViewTest(TestCase):
    fixtures = ['backend']
    urls = 'sendinel.urls'
    
    def setUp (self):
        self.hospital = Hospital.objects.get(current_hospital = True)
        #self.client = Client()
        
    def test_is_valid_appointment(self):
        data = { "date" : "2010-08-12",
                 "recipient" : "0123456789" }
                 
        self.assertTrue(is_valid_appointment(data))
        
        data = { "date" : "2010-08-45",
                 "recipient" : "0123456789" }
                 
        self.assertFalse(is_valid_appointment(data))
        
        data = { "date" : "2010-08-12",
                 "recipient" : "012sdfsdf3456789" }
                 
        self.assertFalse(is_valid_appointment(data))
    
    
    def test_create_appointment_form(self):
        response = self.client.get("/web/appointment/create/")
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, 'name="date_0"')
        self.assertContains(response, 'name="date_1"')
        self.assertNotContains(response, 'name="recipient_type"')
        self.assertNotContains(response, 'name="recipient_id"')
        self.assertNotContains(response, 'name="hospital"')

    def test_create_appointment_submit_validations(self):
        response = self.client.post("/web/appointment/create/", 
                    {'date_0': 'abc',
                    'date_1': 'def',
                    'appointment_type': '',
                    'way_of_communication': 'xyz'  })
        self.failUnlessEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'date',
                            'Enter a valid date/time.')
        self.assertFormError(response, 'form', 'way_of_communication',
                            'Select a valid choice. xyz' \
                            + ' is not one of the available choices.')

    def create_appointment(self, way_of_communication):
        data = {'date_0': '2012-08-12',
                'date_1': '19:02:42',
                'appointment_type': "1",
                'way_of_communication': way_of_communication}

        return self.client.post("/web/appointment/create/", data)
        
    def create_and_save_appointment(self, way_of_communication, phone_number):
        self.create_appointment(way_of_communication)
        
        # fake authentication
        self.client.post(reverse('web_authenticate_phonenumber'),
                    {'number': phone_number})

        return self.client.get(reverse("web_appointment_save"))

    def create_appointment_woc(self, way_of_communication):
        response = self.create_appointment(way_of_communication)
        self.assertRedirects(response, 
                             reverse('web_authenticate_phonenumber') + \
                             "?next=" + \
                             reverse('web_appointment_save'))

        self.assertTrue(self.client.session.has_key('patient'))
        self.assertTrue(self.client.session.has_key('appointment'))
        

    def save_appointment_woc(self, way_of_communication):
        number_of_appointments = HospitalAppointment.objects.count()
        number_of_events = ScheduledEvent.objects.count()
        
        phone_number = "08765934"
        response = self.create_and_save_appointment(way_of_communication, \
                                                    phone_number)
        
        self.failUnlessEqual(response.status_code, 200)
        
        appoint = HospitalAppointment.objects.order_by("id").reverse()[:1][0]
        self.assertEquals(unicode(appoint.recipient.phone_number), phone_number)
        # test that exactly one HospitalAppointment was created
        self.assertEquals(HospitalAppointment.objects.count(),
                            number_of_appointments + 1)
        
        event = ScheduledEvent.objects.order_by("id").reverse()[:1][0]
        self.assertEquals(event.sendable, appoint)
        # test that exactly one ScheduledEvent was created
        self.assertEquals(ScheduledEvent.objects.count(),
                            number_of_events + 1)

    def test_create_appointment_sms(self):
        self.create_appointment_woc('sms')
        
    def test_create_appointment_voice(self):
        self.create_appointment_woc('voice')
        
    def test_create_appointment_bluetooth(self):
         response = self.create_appointment('bluetooth')
         self.assertRedirects(response, 
                              reverse('web_list_devices') + \
                              "?next=" + \
                              reverse('web_appointment_send'))
         self.assertTrue(self.client.session.has_key('patient'))
         self.assertTrue(self.client.session.has_key('appointment'))
         
    def test_save_appointment_sms(self):
         self.save_appointment_woc('sms')

    def test_save_appointment_voice(self):
         self.save_appointment_woc('voice')
