from datetime import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from sendinel.backend.models import ScheduledEvent, HospitalAppointment
from sendinel.backend.models import Hospital, Patient, Doctor
from sendinel import settings

class AppointmentViewTest(TestCase):
    fixtures = ['backend']
    urls = 'web.urls'
    
    def setUp (self):
        self.hospital = Hospital.objects.get(current_hospital = True)
        #self.client = Client()
    
    def test_create_appointment_form(self):
        response = self.client.get("/appointment/create/")
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, 'name="date_0"')
        self.assertContains(response, 'name="date_1"')
        self.assertContains(response, 'name="doctor"')
        self.assertContains(response, 'name="recipient_name"')
        self.assertNotContains(response, 'name="recipient_type"')
        self.assertNotContains(response, 'name="recipient_id"')
        self.assertNotContains(response, 'name="hospital"')

    def test_create_appointment_submit_validations(self):
        response = self.client.post("/appointment/create/", 
                    {'date_0': 'abc',
                    'date_1': 'def',
                    'doctor': '',
                    'recipient_name': '',
                    'way_of_communication': 'xyz'  })
        self.failUnlessEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'doctor',
                            'This field is required.')
        self.assertFormError(response, 'form', 'recipient_name',
                            'This field is required.')
        self.assertFormError(response, 'form', 'date',
                            'Enter a valid date/time.')
        self.assertFormError(response, 'form', 'way_of_communication',
                            'Select a valid choice. xyz' \
                            + ' is not one of the available choices.')

    def test_create_appointment_submit_redirect_sms(self):
        data = {'date_0': '2012-08-12',
                'date_1': '19:02:42',
                'doctor': "1",
                'recipient_name': 'Shiko Taga',
                'way_of_communication': 'sms'}
        number_of_appointments = HospitalAppointment.objects.count()
        response = self.client.post("/appointment/create/", data)
        self.assertRedirects(response, 
                             reverse('web_authenticate_phonenumber') + \
                             "?next=" + \
                             reverse('web_appointment_save'))
        response = self.client.post("/appointment/create/", data, follow=True)
        self.assertTrue(self.client.session.has_key('patient'))
        self.assertTrue(self.client.session.has_key('appointment'))        
 
    def test_create_appointment_submit_redirect_voice(self):
        number_of_appointments = HospitalAppointment.objects.count()
        response = self.client.post("/appointment/create/", 
                    {'date_0': '2012-08-12',
                    'date_1': '19:02:42',
                    'doctor': "1",
                    'recipient_name': 'Shiko Taga',
                    'way_of_communication': 'voice'  })
        self.assertRedirects(response, 
                             reverse('web_authenticate_phonenumber') + \
                             "?next=" + \
                             reverse('web_appointment_save'))
        self.assertTrue(self.client.session.has_key('patient'))
        self.assertTrue(self.client.session.has_key('appointment'))                             

    def test_create_appointment_submit_redirect_voice(self):
        number_of_appointments = HospitalAppointment.objects.count()
        response = self.client.post("/appointment/create/", 
                    {'date_0': '2012-08-12',
                    'date_1': '19:02:42',
                    'doctor': "1",
                    'recipient_name': 'Shiko Taga',
                    'way_of_communication': 'bluetooth'  })
        self.assertRedirects(response, 
                             reverse('web_list_devices') + \
                             "?next=" + \
                             reverse('web_appointment_send'))
        self.assertTrue(self.client.session.has_key('patient'))
        self.assertTrue(self.client.session.has_key('appointment'))                                                          
                             
    def test_save_appointment(self):
        self.client.post("/appointment/create/", 
                    {'date_0': '2012-08-12',
                    'date_1': '19:02:42',
                    'doctor': "1",
                    'recipient_name': 'Shiko Taga',
                    'way_of_communication': 'bluetooth'  })
        response = self.client.get(reverse("web_appointment_save"))
        self.failUnlessEqual(response.status_code, 302)  
        appoint = HospitalAppointment.objects.order_by("id").reverse()[:1][0]
        self.asserEquals(appoint.date, date)
                                                     
            
                #                              
                # self.assertEquals(HospitalAppointment.objects.count(),
                #                     number_of_appointments + 1)
                # appointment = HospitalAppointment.objects \
                #     .order_by("id").reverse()[:1][0]
                # self.assertEquals(appointment.doctor.id, 1)
                # self.assertEquals(appointment.recipient.name, 'Shiko Taga')
                # self.assertEquals(appointment.date, datetime(2012, 8, 12, 19, 02, 42))
                # self.assertEquals(appointment.way_of_communication, "sms")
                # self.assertEquals(appointment.hospital, self.hospital)
                #     

                            
    # def test_create_appointment_scheduled_event_sms(self):
    #     number_of_events = ScheduledEvent.objects.count()
    #     self.client.post("/appointment/create/", 
    #                 {'date_0': '2012-08-12',
    #                 'date_1': '19:02:42',
    #                 'doctor': "1",
    #                 'recipient_name': 'Shiko Taga',
    #                 'way_of_communication': 'sms'  })
    #     self.assertEquals(ScheduledEvent.objects.count(),
    #                         number_of_events + 1)
    # 
    #     
    # def test_create_appointment_scheduled_event_bluetooth(self):
    #     number_of_events = ScheduledEvent.objects.count()
    #     self.client.post("/appointment/create/", 
    #                 {'date_0': '2012-08-12',
    #                 'date_1': '19:02:42',
    #                 'doctor': "1",
    #                 'recipient_name': 'Shiko Taga',
    #                 'way_of_communication': 'bluetooth'  })
    #     self.assertEquals(ScheduledEvent.objects.count(),
    #                         number_of_events)



        