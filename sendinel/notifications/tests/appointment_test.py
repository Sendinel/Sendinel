from datetime import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from sendinel.backend.models import Hospital, Patient, ScheduledEvent
from sendinel.notifications.models import HospitalAppointment, AppointmentType
from sendinel.settings import AUTH
from sendinel.web.forms import  NotificationValidationForm2, \
                                DateValidationForm
from sendinel import settings

class AppointmentViewTest(TestCase):
    fixtures = ['backend_test']
    urls = 'sendinel.urls'
    
    def setUp (self):
        self.hospital = Hospital.objects.get(current_hospital = True)
        self.client = Client()
        
    def test_notification_form_validation(self):
        data = {"phone_number" : "0123456789",
                "way_of_communication" : "bluetooth"}
        form = NotificationValidationForm2(data)
        self.assertTrue(form.is_valid())
        
        date = {"date" : "2010-08-12 12:00"}
        form_date = DateValidationForm(date)
        self.assertTrue(form_date.is_valid())

        
        data = { "phone_number" : "0123456rttddbh789",
                 "way_of_communication" : "Bluetooth" }
        form = NotificationValidationForm2(data)
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form['phone_number'].errors), 1)
        self.assertEquals(len(form['way_of_communication'].errors), 1)
        
        date = {"date" : "2010-08-45 12:00"}
        form_date = DateValidationForm(date)
        self.assertFalse(form_date.is_valid())         
        self.assertEquals(len(form_date['date'].errors), 1)
    
    
    
    
    def create_appointment_form(self, appointment_type_id):
        appointment_type = AppointmentType.objects.get(pk=appointment_type_id)
        response = self.client.get(reverse('web_appointment_create', \
                kwargs={"appointment_type_name": appointment_type.name }))
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, 'name="phone_number"')
        self.assertContains(response, 'name="way_of_communication"')
        return response

    
    
    def test_create_appointment_form_notify_immediately(self):
        #labresult
        response = self.create_appointment_form(3)
        self.assertNotContains(response, 'name="date"')
       
    
    def test_create_appointment_form_dont_notify_immediately(self):
        #vaccination
        response = self.create_appointment_form(1)
        self.assertContains(response, 'name="date"')

    
    
    def test_create_appointment_submit_validations(self):
        appointment_type = AppointmentType.objects.get(pk=1) #vaccination
        response = self.client.post(reverse('web_appointment_create', \
            kwargs={"appointment_type_name": appointment_type.name }), 
                {'date': '2012-08-12',
                 'phone_number': '01733685224',
                 'way_of_communication':'sms'  })
        self.assertEquals(response.status_code, 302)
            
        response = self.client.post(reverse('web_appointment_create', \
                kwargs={"appointment_type_name": appointment_type.name }), 
                    {'date': '2012-08-12',
                     'phone_number': '01733assr685224',
                      'way_of_communication':'spoois' })

        self.assertContains(response, 'Please enter numbers only')

        response = self.client.post(reverse('web_appointment_create', \
            kwargs={"appointment_type_name": appointment_type.name }), 
                {'date': '2012-08-12',
                    'phone_number': '685224',
                    'way_of_communication':'sms'  })
        self.assertContains(response, 'Please enter a cell phone number.')


        

    def create_appointment(self, way_of_communication):
        appointment_type = AppointmentType.objects.get(pk=1) #vaccination
        self.client.get(reverse('web_appointment_create', \
                kwargs={"appointment_type_name": appointment_type.name }))
        
        data = {'date': '2012-08-12',
                'phone_number': '01733685224',
                'way_of_communication': way_of_communication}
        return self.client.post(reverse('web_appointment_create', \
                kwargs = {"appointment_type_name": appointment_type.name }), data)
        
    def create_and_save_appointment(self, way_of_communication, phone_number):
        self.create_appointment(way_of_communication)
        
        patient = Patient()
        patient.phone_number = phone_number
        # fake authentication
        self.client.post(reverse('web_authenticate_phonenumber'), \
                    {'patient': patient})

        return self.client.get(reverse("web_appointment_save"))

    def create_appointment_woc(self, way_of_communication):
        response = self.create_appointment(way_of_communication)
       
        if AUTH:
            self.assertRedirects(response, 
                             reverse('web_authenticate_phonenumber') + \
                             "?next=" + \
                             reverse('web_appointment_save'))

        self.assertTrue(self.client.session.has_key('patient'))
        self.assertTrue(self.client.session.has_key('appointment'))
        

    def save_appointment_woc(self, way_of_communication):
        
        number_of_appointments = HospitalAppointment.objects.count()
        number_of_events = ScheduledEvent.objects.count()
        
        phone_number = "01733685224"
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
         
    def test_create_appointment_with_current_date(self):
        appointment_type = AppointmentType.objects.get(pk=3) #labresults
        response = self.client.post(reverse('web_appointment_create', \
            kwargs={"appointment_type_name": appointment_type.name }), 
                {'phone_number': '01733685224',
                 'way_of_communication':'sms'  })
        # validations test if date is correct. 
        # If not, there will be no 302 status code
        self.assertEquals(response.status_code, 302)
        
        
